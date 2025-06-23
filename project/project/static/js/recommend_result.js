document.addEventListener('DOMContentLoaded', () => {
    const priceText = document.getElementById('price-text');
    const plusBtn = document.querySelectorAll('.price-btn')[1];
    const minusBtn = document.querySelectorAll('.price-btn')[0];
  
    // 숫자만 추출하여 현재 가격으로 저장
    let currentPrice = parseInt(priceText.innerText.replace(/[^0-9]/g, ''));
  
    // 초기 가격에 콤마 추가
    priceText.innerText = currentPrice.toLocaleString() + '원';
  
    // + 버튼 클릭 시
    plusBtn.addEventListener('click', () => {
      currentPrice += 1000;
      priceText.innerText = currentPrice.toLocaleString() + '원';
    });
  
    // - 버튼 클릭 시 (0원 미만으로 내려가지 않도록)
    minusBtn.addEventListener('click', () => {
      if (currentPrice >= 1000) {
        currentPrice -= 1000;
        priceText.innerText = currentPrice.toLocaleString() + '원';
      }
    });
  });