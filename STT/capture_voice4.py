from RealtimeSTT import AudioToTextRecorder
import logging, time

if __name__ == '__main__':
# def main():
    WAITER = 3
    INPUT_WAITER = 2
    countt = 0

    def recording_started():
        print("Speak now...")

    def recording_finished():
        print("Speech end detected... transcribing...")

    recorder_config = {
        'spinner': False,
        # 'model': 'large-v2',
        'model':"base",
        'language': 'en',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0.4,
        'min_length_of_recording': 0.5,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.2,
        # 'realtime_model_type': 'tiny.en',
        'realtime_model_type': 'base.en',

        # 'on_realtime_transcription_update': text_detected, 
        # 'on_realtime_transcription_stabilized': text_detected,
        # 'level' : logging.DEBUG,
        # 'wake_words':"hey google",
        # 'on_wakeword_detected' : recording_started, 
        # 'on_recording_stop' : recording_finished
    }


    # with AudioToTextRecorder(spinner=False, level=logging.DEBUG, model="tiny.en", language="en", wake_words="hey google", on_wakeword_detected=recording_started, on_recording_stop=recording_finished
    # ) as recorder:
    with AudioToTextRecorder(**recorder_config) as recorder:
        # print('Say "Jarvis" then speak.')
        init_text = ""
        full_sentences = []
        while True:
            init_text = " ".join(full_sentences)
            # user_text = recorder.text()
            recorder.start()

            if countt == 0:
                print(f"Waiting {WAITER} sec...")
                time.sleep(WAITER)
            else:
                print(f"Waiting {INPUT_WAITER} sec...")
                time.sleep(INPUT_WAITER)
            
            user_text = recorder.text()

            if len(user_text) > 0:
                full_sentences.append(user_text)

            if len(" ".join(full_sentences)) != len(init_text):
                countt += 1
                continue
            else:
                recorder.stop()
                break

        print("Done. Now we should exit.")

        print("You said - ")
        print(" ".join(full_sentences))