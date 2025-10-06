export default function useFullscreen() {
  const enter = () => {
    const el: any = document.documentElement;
    if (el.requestFullscreen) el.requestFullscreen();
    else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
  };
  const exit = () => {
    const d: any = document;
    if (d.exitFullscreen) d.exitFullscreen();
    else if (d.webkitExitFullscreen) d.webkitExitFullscreen();
  };
  const toggle = () => {
    const d: any = document;
    if (!d.fullscreenElement && !d.webkitFullscreenElement) enter();
    else exit();
  };
  return { enter, exit, toggle };
}

