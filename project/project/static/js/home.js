document.getElementById("price-form").addEventListener("submit", function (e) {
    const priceInput = document.getElementById("price-input");
    const warning = document.getElementById("price-warning");
    const priceValue = Number(priceInput.value);

    if (!priceValue || priceValue < 1000) {
      e.preventDefault(); // 폼 제출 막기
      warning.style.display = "block"; // 경고 표시
    } else {
      warning.style.display = "none"; // 통과 시 경고 숨기기
    }
  });

