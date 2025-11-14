
# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

#load_dotenv()

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    # Check if audio filepath is provided
    if audio_filepath is None:
        speech_to_text_output = "No audio input provided"
    else:
        try:
            speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                       audio_filepath=audio_filepath,
                                                       stt_model="whisper-large-v3")
        except Exception as e:
            speech_to_text_output = f"Error transcribing audio: {str(e)}"

    # Handle the image input
    if image_filepath:
        try:
            doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct") #model="meta-llama/llama-4-maverick-17b-128e-instruct") 
        except Exception as e:
            doctor_response = f"Error analyzing image: {str(e)}"
    else:
        doctor_response = "No image provided for me to analyze"

    # Check if ElevenLabs API key is available
    if os.environ.get("ELEVEN_API_KEY"):
        try:
            voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3")
        except Exception as e:
            voice_of_doctor = f"Error generating speech: {str(e)}"
    else:
        try:
            voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3")
        except Exception as e:
            voice_of_doctor = f"Error generating speech: {str(e)}"

    return speech_to_text_output, doctor_response, voice_of_doctor


# Create the interface with better styling
with gr.Blocks(title="AI Doctor with Vision and Voice", theme=gr.themes.Soft()) as iface:
    gr.Markdown("# 🏥 AI Doctor with Vision and Voice")
    gr.Markdown("Upload a medical image and ask a question to get AI-powered medical analysis with voice response.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📤 Input")
            audio_input = gr.Audio(
                sources=["microphone"], 
                type="filepath",
                label="Record your medical question"
            )
            image_input = gr.Image(
                type="filepath",
                label="Upload medical image"
            )
            submit_btn = gr.Button("🔍 Analyze", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### 📋 Results")
            speech_output = gr.Textbox(
                label="Your Question (Speech to Text)",
                lines=3
            )
            doctor_output = gr.Textbox(
                label="Doctor's Response",
                lines=5
            )
            audio_output = gr.Audio(
                label="Doctor's Voice Response"
            )
    
    gr.Markdown("---")
    gr.Markdown("### ℹ️ Instructions")
    gr.Markdown("""
    1. **Record Audio**: Click the microphone button and speak your medical question
    2. **Upload Image**: Upload a medical image (X-ray, skin condition, etc.)
    3. **Click Analyze**: Get AI-powered medical analysis with voice response
    4. **Listen**: Click the play button to hear the doctor's response
    """)
    
    gr.Markdown("### ⚠️ Disclaimer")
    gr.Markdown("This is for educational purposes only. Always consult a real healthcare professional for medical advice.")
    
    # Connect the submit button
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_output, doctor_output, audio_output]
    )

iface.launch(debug=True, share=False)

#http://127.0.0.1:7860