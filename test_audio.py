#!/usr/bin/env python3
"""
Test script to verify audio generation functionality
"""

import os
from dotenv import load_dotenv
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# Load environment variables
load_dotenv()

def test_gtts():
    """Test gTTS audio generation"""
    print("Testing gTTS audio generation...")
    try:
        result = text_to_speech_with_gtts(
            input_text="Hello, this is a test of the AI doctor voice system.",
            output_filepath="test_gtts.mp3"
        )
        print(f"✅ gTTS test successful: {result}")
        return True
    except Exception as e:
        print(f"❌ gTTS test failed: {e}")
        return False

def test_elevenlabs():
    """Test ElevenLabs audio generation"""
    print("Testing ElevenLabs audio generation...")
    if not os.environ.get("ELEVEN_API_KEY"):
        print("⚠️  ElevenLabs API key not found, skipping test")
        return False
    
    try:
        result = text_to_speech_with_elevenlabs(
            input_text="Hello, this is a test of the AI doctor voice system using ElevenLabs.",
            output_filepath="test_elevenlabs.mp3"
        )
        print(f"✅ ElevenLabs test successful: {result}")
        return True
    except Exception as e:
        print(f"❌ ElevenLabs test failed: {e}")
        return False

def main():
    print("🎵 Audio Generation Test Suite")
    print("=" * 40)
    
    # Test gTTS (should always work)
    gtts_success = test_gtts()
    
    # Test ElevenLabs (if API key is available)
    elevenlabs_success = test_elevenlabs()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"gTTS: {'✅ PASS' if gtts_success else '❌ FAIL'}")
    print(f"ElevenLabs: {'✅ PASS' if elevenlabs_success else '❌ FAIL'}")
    
    if gtts_success:
        print("\n🎉 At least one audio generation method is working!")
        print("You can now run the main application with: python gradio_app.py")
    else:
        print("\n⚠️  Audio generation tests failed. Please check your setup.")

if __name__ == "__main__":
    main()