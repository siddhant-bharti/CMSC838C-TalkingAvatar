



using UnityEngine;
using System.IO;
using System.Collections;
using UnityEngine.Networking;
using System;
using System.Text;
using UnityEngine.UI;
using System.Data;
using TMPro;

public class AudioRecorder : MonoBehaviour
{
    public int recordDuration = 10; // Maximum duration of the recording in seconds
    private AudioClip recordedAudio;
    private bool isRecording = false;
    private string inputFilePath;
    private string outputFilePath;

    private AudioSource audioSource;
    public TextMeshProUGUI statusText;

    void Start()
    {
        audioSource = GetComponent<AudioSource>();
        if (audioSource == null)
        {
            audioSource = gameObject.AddComponent<AudioSource>();
        }
        UpdateStatus("Ready to record");
    }

    void OnGUI()
    {
    }

    void Update()
    {
        // Handle space bar press to start/stop recording
        if (Input.GetKeyDown(KeyCode.Space))
        {
            if (!isRecording)
            {
                isRecording = true;
                StartRecording();
            }
            else
            {

                Debug.Log("Space bar - stop");
                isRecording = false;
                StopRecording();
            }
        }



    }

    void StartRecording()
    {
        if (Microphone.devices.Length > 0)
        {
            UpdateStatus("Recording...");
            string microphone = Microphone.devices[0];
            recordedAudio = Microphone.Start(microphone, true, recordDuration, 44100);
            Debug.Log("Recording started with " + microphone);
        }
        else
        {
            Debug.LogError("No microphone devices found!");
        }
    }

    IEnumerator StopRecordingAfterDelay(int delay)
    {
        yield return new WaitForSeconds(delay);
        StopRecording();
    }

    void StopRecording()
    {
        if (Microphone.IsRecording(null))
        {
            UpdateStatus("Recording stopped. Processing...");
            Microphone.End(null);
            Debug.Log("Recording stopped.");
            SaveRecordingToDisk(recordedAudio);
        }
    }

    void UpdateStatus(string message)
    {
        if (statusText != null)
        {
            Debug.Log("Status Text is Updated");
            statusText.text = message;
        }
        else
        {
            Debug.Log("Status Text component is not set.");
        }
    }

    void PlayOutput()
    {
        if (File.Exists(outputFilePath))
        {
            AudioClip clip = WavUtility.ToAudioClip(outputFilePath);
            audioSource.clip = clip;

            UpdateStatus("Playing Sound");
            audioSource.Play();
            StartCoroutine(WaitForAudioToEnd());

            Debug.Log("Playback output started.");
        }
        else
        {
            Debug.LogError("Output file not found.");
        }
    }

    IEnumerator WaitForAudioToEnd()
    {
        while (audioSource.isPlaying)
        {
            yield return null;
        }
        UpdateStatus("Waiting...");
        Debug.Log("Playback output finished.");
        // Continue other tasks here
    }

    void SaveRecordingToDisk(AudioClip clip)
    {
        inputFilePath = Path.Combine(Application.persistentDataPath, "input.wav");
        byte[] wavFile = WavUtility.FromAudioClip(clip);
        WavUtility.Save(inputFilePath, wavFile);
        Debug.Log($"Saved recording to {inputFilePath}");
        StartCoroutine(SendAudioFile(inputFilePath));
    }

    IEnumerator SendAudioFile(string path)
    {
        byte[] fileData = File.ReadAllBytes(path);
        WWWForm form = new WWWForm();
        form.AddBinaryData("audio", fileData, "input.wav", "audio/wav");

        using (UnityWebRequest www = UnityWebRequest.Post("https://fac9-128-8-120-3.ngrok-free.app/process-audio/", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Failed to send audio file: {www.error}");
            }
            else
            {
                Debug.Log("File successfully sent to the server");
                SaveOutputFromAPI(www.downloadHandler.data);
            }
        }
    }

    void SaveOutputFromAPI(byte[] data)
    {
        outputFilePath = Path.Combine(Application.persistentDataPath, "output.wav");
        File.WriteAllBytes(outputFilePath, data);
        Debug.Log($"Output saved to {outputFilePath}");
        PlayOutput(); // Automatically play the output after saving
    }
}

/*public class AudioRecorder : MonoBehaviour
{
    public int recordDuration = 10; // Maximum duration of the recording in seconds
    private AudioClip recordedAudio;
    private bool isRecording = false;
    private bool isRecordingComplete = false;
    private string inputFilePath;
    private string outputFilePath;

    private AudioSource audioSource;


    void Start()
    {
        audioSource = GetComponent<AudioSource>();
        if (audioSource == null)
        {
            audioSource = gameObject.AddComponent<AudioSource>();
        }
    }

    void OnGUI()
    {
        if (!isRecording && GUI.Button(new Rect(10, 10, 100, 30), "Record"))
        {
            StartRecording();
        }
        if (isRecording && GUI.Button(new Rect(10, 50, 100, 30), "Stop"))
        {
            StopRecording();
        }
        if (GUI.Button(new Rect(10, 90, 100, 30), "Play Recorded"))
        {
            PlayRecordedInput();
        }
        if (isRecordingComplete && GUI.Button(new Rect(10, 130, 100, 30), "Play Output"))
        {
            PlayRecordedOutput();
        }
    }

    void StartRecording()
    {
        if (Microphone.devices.Length > 0)
        {
            string microphone = Microphone.devices[0];
            recordedAudio = Microphone.Start(microphone, false, recordDuration, 44100);
            isRecording = true;
            isRecordingComplete = false;
            Debug.Log("Recording started with " + microphone);
        }
        else
        {
            Debug.LogError("No microphone devices found!");
        }
    }

    void StopRecording()
    {
        if (Microphone.IsRecording(null))
        {
            Microphone.End(null);
            isRecording = false;
            isRecordingComplete = true;
            Debug.Log("Recording stopped.");
            SaveRecordingToDisk(recordedAudio);
        }
    }

    void PlayRecordedInput()
    {
        if (File.Exists(inputFilePath))
        {
            AudioClip clip = WavUtility.ToAudioClip(inputFilePath);
            audioSource.clip = clip;
            audioSource.Play();
            Debug.Log("Playback started.");
        }
        else
        {
            Debug.LogError("Audio file not found!");
        }
    }

    void PlayRecordedOutput()
    {
        if (File.Exists(outputFilePath))
        {
            AudioSource audioSource = GetComponent<AudioSource>();
            if (audioSource == null)
            {
                audioSource = gameObject.AddComponent<AudioSource>();
            }
            audioSource.clip = WavUtility.ToAudioClip(outputFilePath);
            audioSource.Play();
            Debug.Log("Playback output started.");
        }
        else
        {
            Debug.LogError("Output file not found.");
        }
    }


    void SaveRecordingToDisk(AudioClip clip)
    {
        // Set the file path where the WAV file will be saved
        inputFilePath = Path.Combine("input.wav");
        
        // Convert AudioClip to WAV format byte array using WavUtility
        byte[] wavFile = WavUtility.FromAudioClip(clip);
        
        // Save the WAV file to disk
        WavUtility.Save(inputFilePath, wavFile);
        
        // Log the file save and start the coroutine to send the file
        Debug.Log($"Saved recording to {inputFilePath}");
        StartCoroutine(SendAudioFile(inputFilePath));
    }

    IEnumerator SendAudioFile(string path)
    {
        byte[] fileData = File.ReadAllBytes(path);
        WWWForm form = new WWWForm();
        form.AddBinaryData("audio", fileData, "input.wav", "audio/wav");

        using (UnityWebRequest www = UnityWebRequest.Post("https://6b8d-128-8-120-3.ngrok-free.app/process-audio/", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Failed to send audio file: {www.error}");
            }
            else
            {
                Debug.Log("File successfully sent to the server");
                SaveOutputFromAPI(www.downloadHandler.data);
            }
        }
    }

    void SaveOutputFromAPI(byte[] data)
    {
        outputFilePath = Path.Combine("output.wav");
        File.WriteAllBytes(outputFilePath, data);
        Debug.Log($"Output saved to {outputFilePath}");
    }
}*/

public static class WavUtility
{
    // Convert an AudioClip to a WAV file.
    public static byte[] FromAudioClip(AudioClip audioClip, bool trim = false)
    {
        var samples = new float[audioClip.samples * audioClip.channels];
        audioClip.GetData(samples, 0);

        Byte[] wavFile;
        using (var stream = new MemoryStream())
        {
            using (var writer = new BinaryWriter(stream))
            {
                writer.Write(Encoding.UTF8.GetBytes("RIFF"));
                writer.Write(0);
                writer.Write(Encoding.UTF8.GetBytes("WAVE"));
                writer.Write(Encoding.UTF8.GetBytes("fmt "));
                writer.Write(16);
                writer.Write((short)1); // PCM
                writer.Write((short)audioClip.channels);
                writer.Write(audioClip.frequency);
                writer.Write(audioClip.frequency * audioClip.channels * 2); // byte rate
                writer.Write((short)(audioClip.channels * 2)); // block align
                writer.Write((short)16); // bits per sample
                writer.Write(Encoding.UTF8.GetBytes("data"));
                writer.Write(samples.Length * 2); // bytes in data

                foreach (var sample in samples)
                {
                    writer.Write((short)(sample * 32767)); // convert float to short
                }

                writer.Seek(4, SeekOrigin.Begin);
                writer.Write((int)(stream.Length - 8)); // Final size of WAV file
            }
            wavFile = stream.ToArray();
        }

        return wavFile;
    }

    // Save WAV data to a file
    public static void Save(string filepath, byte[] wavFile)
    {
        File.WriteAllBytes(filepath, wavFile);
    }

    // Convert a WAV file to an AudioClip
    public static AudioClip ToAudioClip(string filePath)
    {
        byte[] fileData = File.ReadAllBytes(filePath);
        int channels = BitConverter.ToInt16(fileData, 22);
        int frequency = BitConverter.ToInt32(fileData, 24);
        int pos = 12;

        // Find data chunk
        while (!(fileData[pos] == 100 && fileData[pos + 1] == 97 && fileData[pos + 2] == 116 && fileData[pos + 3] == 97))
        {
            pos += 4;
            int chunkSize = fileData[pos] + fileData[pos + 1] * 256 + fileData[pos + 2] * 65536 + fileData[pos + 3] * 16777216;
            pos += 4 + chunkSize;
        }
        pos += 8;

        // Get the data
        int sampleCount = (fileData.Length - pos) / 2;
        float[] samples = new float[sampleCount];
        int sampleIndex = 0;

        while (pos < fileData.Length)
        {
            short sample = BitConverter.ToInt16(fileData, pos);
            samples[sampleIndex] = sample / 32768f; // convert short to float
            sampleIndex++;
            pos += 2;
        }

        AudioClip audioClip = AudioClip.Create("loadedClip", sampleCount, channels, frequency, false);
        audioClip.SetData(samples, 0);

        return audioClip;
    }
}