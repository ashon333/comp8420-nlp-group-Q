// Authentication management for Congo Shop

function getNickname() {
  return localStorage.getItem('nickname') || null;
}

function loginUser(nickname) {
  localStorage.setItem('nickname', nickname.trim());
}

function logoutUser() {
  localStorage.removeItem('nickname');
  window.location.href = 'login.html';
}

// Redirect checking based on login state
// To prevent layout flashing, call this in the head of your html files
function requireAuth(isLoginPage = false) {
  const nickname = getNickname();
  if (isLoginPage) {
    if (nickname) {
      window.location.href = 'index.html';
    }
  } else {
    if (!nickname) {
      window.location.href = 'login.html';
    }
  }
}
