
document.addEventListener('DOMContentLoaded', () => {
  const boxEls = document.querySelectorAll('.rolling');
  const chars = ['🍕', '🍜', '🍱', '🥪', '🍛', '🍔', '🥗', '🍙', '🍤', '🍩', '?'];

  let interval = setInterval(() => {
    boxEls.forEach(box => {
      box.textContent = chars[Math.floor(Math.random() * chars.length)];
    });
  }, 100);

  setTimeout(() => {
    clearInterval(interval);
    const redirectUrl = document.body.dataset.redirectUrl;
    window.location.href = redirectUrl;
  }, 2000);
});

