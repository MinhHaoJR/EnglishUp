import { act, renderHook, waitFor } from '@testing-library/react';
import { useRecorder } from './useRecorder';
afterEach(() => vi.unstubAllGlobals());
test('permission denial becomes a recoverable error', async () => {
  vi.stubGlobal('MediaRecorder', class {});
  Object.defineProperty(navigator, 'mediaDevices', {
    configurable: true,
    value: {
      getUserMedia: vi.fn().mockRejectedValue(new DOMException('Denied', 'NotAllowedError')),
    },
  });
  const { result } = renderHook(() => useRecorder('en-US'));
  await act(() => result.current.start(false));
  expect(result.current.error).toBe('NotAllowedError');
  expect(result.current.recording).toBe(false);
  expect(result.current.pending).toBe(false);
});
test('recording creates a session URL and releases microphone and URL on unmount', async () => {
  const trackStop = vi.fn();
  const stream = { getTracks: () => [{ stop: trackStop }] };
  Object.defineProperty(navigator, 'mediaDevices', {
    configurable: true,
    value: { getUserMedia: vi.fn().mockResolvedValue(stream) },
  });
  class FakeRecorder {
    state = 'inactive';
    mimeType = 'audio/webm';
    ondataavailable?: (event: { data: Blob }) => void;
    onstop?: () => void;
    onerror?: () => void;
    start() {
      this.state = 'recording';
    }
    stop() {
      this.state = 'inactive';
      this.ondataavailable?.({ data: new Blob(['test audio']) });
      this.onstop?.();
    }
  }
  vi.stubGlobal('MediaRecorder', FakeRecorder);
  const create = vi.fn().mockReturnValue('blob:session-audio');
  const revoke = vi.fn();
  vi.stubGlobal(
    'URL',
    class extends URL {
      static createObjectURL = create;
      static revokeObjectURL = revoke;
    },
  );
  const { result, unmount } = renderHook(() => useRecorder('en-US'));
  await act(() => result.current.start(false));
  expect(result.current.recording).toBe(true);
  act(() => result.current.stop());
  await waitFor(() => expect(result.current.audio).toBe('blob:session-audio'));
  expect(trackStop).toHaveBeenCalled();
  unmount();
  expect(revoke).toHaveBeenCalledWith('blob:session-audio');
});
