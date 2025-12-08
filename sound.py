import numpy as np
import pygame

# Mixer settings (can be adjusted for quality/performance)
# Pygame defaults are usually 44100 Hz, -16 bit stereo, 2 channels, 1024 byte buffer
# We'll use mono for simplicity for now.
# pygame.mixer.pre_init(44100, -16, 1, 1024) # Sample rate, bit depth, channels, buffer size

# To ensure the mixer is initialized, although main.py calls pygame.init()
# it's good practice to ensure the mixer part is ready here if this module
# were ever used standalone.
if not pygame.mixer.get_init():
    pygame.mixer.init()


def generate_tone_array(frequency, duration, volume=0.5, sample_rate=44100):
    """
    Generates a sine wave tone as a NumPy array.
    frequency: frequency of the tone in Hz
    duration: duration of the tone in seconds
    volume: amplitude of the tone (0.0 to 1.0)
    sample_rate: samples per second
    """
    num_samples = int(sample_rate * duration)
    time = np.linspace(0, duration, num_samples, False)
    amplitude = (2**15 - 1) * volume  # Max amplitude for 16-bit audio

    # Generate a sine wave
    data = amplitude * np.sin(2 * np.pi * frequency * time)

    # Apply a simple envelope to avoid clicks at start/end
    envelope = np.ones(num_samples)
    fade_samples = min(
        int(0.005 * sample_rate), num_samples // 4
    )  # 5ms fade or 1/4 of sound
    if fade_samples > 0:
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    data = data * envelope

    # Convert to 16-bit integers for Pygame
    sound_array = data.astype(np.int16)
    return sound_array


def _make_sound_buffer(sound_array_1d):
    """
    Converts a 1D numpy array of samples into a pygame Sound object,
    handling stereo/mono mixer settings automatically.
    """
    mixer_settings = pygame.mixer.get_init()
    if mixer_settings:
        channels = mixer_settings[2]
        if channels == 2:
            # Stereo: Stack the 1D array to make it (N, 2)
            sound_buffer = np.column_stack((sound_array_1d, sound_array_1d))
        else:
            # Mono: Ensure it is (N, 1)
            sound_buffer = sound_array_1d.reshape(-1, 1)
    else:
        # Fallback if mixer not initialized (shouldn't happen), assume mono
        sound_buffer = sound_array_1d.reshape(-1, 1)

    return pygame.sndarray.make_sound(sound_buffer)


def play_tone(frequency, duration, volume=0.5, sample_rate=44100):
    """
    Generates and plays a sine wave tone.
    """
    sound_array = generate_tone_array(frequency, duration, volume, sample_rate)

    sound = _make_sound_buffer(sound_array)
    sound.play()
    return sound  # Return sound object in case it needs to be stopped or managed


def stop_all_sounds():
    """Stops all currently playing sounds."""
    pygame.mixer.stop()


def play_drop_sound():
    """Plays a sound for dropping a piece."""
    # A short, descending tone for a comedic drop effect
    freq1 = 300
    freq2 = 200
    duration = 0.1
    volume = 0.3  # Slightly quieter
    sample_rate = 44100

    # Generate a short descending slide
    num_samples = int(sample_rate * duration)

    # Linear frequency glide
    frequencies = np.linspace(freq1, freq2, num_samples)

    # Use phase accumulation for smooth frequency sweep (integrate instantaneous frequency)
    dt = 1.0 / sample_rate
    phase = np.cumsum(2 * np.pi * frequencies * dt)

    # Generate the waveform using accumulated phase
    data = (2**15 - 1) * volume * np.sin(phase)

    # Apply a simple envelope to avoid clicks at start/end
    envelope = np.ones(num_samples)
    fade_samples = min(
        int(0.005 * sample_rate), num_samples // 4
    )  # 5ms fade or 1/4 of sound
    if fade_samples > 0:
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    data = data * envelope

    sound_array = data.astype(np.int16)
    sound = _make_sound_buffer(sound_array)
    sound.play()


def play_win_sound():
    """Plays a sound for winning the game."""
    # A short, ascending, triumphant (but still silly) jingle
    melody = [(440, 0.1), (554, 0.1), (659, 0.2)]  # A, C#, E
    for freq, dur in melody:
        play_tone(freq, dur, volume=0.4)
        pygame.time.wait(int(dur * 1000) + 10)


def play_invalid_move_sound():
    """Plays a sound for an invalid move."""
    # A short, sharp "buzz" or "boop"
    play_tone(150, 0.1, volume=0.5)


def play_start_game_sound():
    """Plays a short, playful jingle at the start of the game."""
    # A short, playful jingle
    melody = [(523, 0.1), (659, 0.1), (784, 0.1), (1047, 0.2)]  # C5, E5, G5, C6
    for freq, dur in melody:
        play_tone(freq, dur, volume=0.3)
        pygame.time.wait(int(dur * 1000) + 10)


def play_tie_sound():
    """Plays a sound for a tie game (womp womp)."""
    # A sad, descending trombone-like effect
    melody = [(196, 0.3), (185, 0.3), (174, 0.3), (164, 0.6)]  # G3, F#3, F3, E3
    for freq, dur in melody:
        play_tone(freq, dur, volume=0.4)
        pygame.time.wait(int(dur * 1000) + 10)


# Example usage (for testing purposes, won't run when imported)
if __name__ == "__main__":
    print("Playing start game sound...")
    play_start_game_sound()
    pygame.time.wait(1000)

    print("Playing drop sound...")
    play_drop_sound()
    pygame.time.wait(500)

    print("Playing invalid move sound...")
    play_invalid_move_sound()
    pygame.time.wait(500)

    print("Playing win sound...")
    play_win_sound()
    pygame.time.wait(1000)

    print("Playing tie sound...")
    play_tie_sound()
    pygame.time.wait(1000)

    print("Done playing sounds.")
    pygame.quit()  # Only quit if this script is run standalone
