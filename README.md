# AI Doctor with Vision and Voice

An AI-powered medical consultation app that can analyze medical images and respond with voice output.

## Features

- **Speech-to-Text**: Convert patient voice input to text using Groq API
- **Image Analysis**: Analyze medical images using AI vision models
- **Text-to-Speech**: Generate doctor's response in voice using ElevenLabs or gTTS
- **Web Interface**: User-friendly Gradio interface

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirement.txt
```

### 2. Set up API Keys

Create a `.env` file in the project root with your API keys:

```env
# Groq API Key for speech-to-text
GROQ_API_KEY=your_groq_api_key_here

# ElevenLabs API Key for text-to-speech (optional)
ELEVEN_API_KEY=your_elevenlabs_api_key_here
```

### 3. Get API Keys

- **Groq API Key**: Sign up at [Groq Console](https://console.groq.com/) and get your API key
- **ElevenLabs API Key**: Sign up at [ElevenLabs](https://elevenlabs.io/) and get your API key (optional)

### 4. Run the Application

```bash
python gradio_app.py
```

The app will be available at `http://127.0.0.1:7860`

## How to Use

1. **Record Audio**: Click the microphone button to record your medical question
2. **Upload Image**: Upload a medical image for analysis
3. **Get Response**: The AI doctor will analyze the image and respond with voice output

## Troubleshooting

### Common Issues

1. **"No audio input provided"**: Make sure to record audio before submitting
2. **"GROQ_API_KEY is required"**: Set your Groq API key in the `.env` file
3. **"ELEVEN_API_KEY environment variable is not set"**: The app will fallback to gTTS if ElevenLabs key is not provided

### Error Handling

The app now includes proper error handling for:
- Missing audio input
- Missing API keys
- Network errors
- File processing errors

## File Structure

- `gradio_app.py`: Main application with Gradio interface
- `brain_of_the_doctor.py`: Image analysis functionality
- `voice_of_the_patient.py`: Speech-to-text functionality
- `voice_of_the_doctor.py`: Text-to-speech functionality
- `requirement.txt`: Python dependencies