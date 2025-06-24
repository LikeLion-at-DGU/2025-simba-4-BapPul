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

  function toggleDropdown() {
    const options = document.getElementById("radius-options");
    options.style.display = options.style.display === "block" ? "none" : "block";
  }
  
  document.addEventListener("click", function (event) {
    const dropdown = document.querySelector(".radius-dropdown");
    const options = document.getElementById("radius-options");
    if (!dropdown.contains(event.target)) {
      options.style.display = "none";
    }
  });
  

