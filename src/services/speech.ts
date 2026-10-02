import type { Settings } from './storage';
export function stopSpeech() {
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
}
export function speak(
  text: string,
  settings: Pick<Settings, 'accent' | 'rate'>,
  speaker = 0,
  onError?: () => void,
) {
  if (!('speechSynthesis' in window)) return false;
  stopSpeech();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = settings.accent;
  utterance.rate = settings.rate;
  const voices = speechSynthesis.getVoices().filter((v) => v.lang === settings.accent);
  if (voices.length) utterance.voice = voices[speaker % voices.length];
  utterance.pitch = voices.length < 2 ? (speaker % 2 ? 1.12 : 0.94) : 1;
  utterance.onerror = (e) => {
    if (e.error !== 'canceled' && e.error !== 'interrupted') onError?.();
  };
  speechSynthesis.speak(utterance);
  return true;
}
export function speakLines(
  lines: { speaker: string; text: string }[],
  settings: Pick<Settings, 'accent' | 'rate'>,
  onError: () => void,
  speakers = [...new Set(lines.map((l) => l.speaker))],
) {
  if (!('speechSynthesis' in window)) {
    onError();
    return;
  }
  stopSpeech();
  const voices = speechSynthesis.getVoices().filter((v) => v.lang === settings.accent);
  for (const line of lines) {
    const index = speakers.indexOf(line.speaker);
    const u = new SpeechSynthesisUtterance(line.text);
    u.lang = settings.accent;
    u.rate = settings.rate;
    u.pitch = voices.length < 2 ? (index % 2 ? 1.12 : 0.94) : 1;
    if (voices.length) u.voice = voices[index % voices.length];
    u.onerror = (e) => {
      if (e.error !== 'canceled' && e.error !== 'interrupted') onError();
    };
    speechSynthesis.speak(u);
  }
}
