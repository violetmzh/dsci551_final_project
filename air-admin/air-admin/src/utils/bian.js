function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].split('=');
      if (cookie[0] === name) {
        return cookie[1];
      }
    }
    return null;
  }


  function storeInLocalStorage(name, value) {
    localStorage.setItem(name, value);
  }

  function eraseCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  }




  function migrateCookieToLocalStorage(cookieName) {
    const cookieValue = getCookie(cookieName);
    console.log(cookieValue,'cookieValue');
    if (cookieValue !== null) {
      storeInLocalStorage(cookieName, cookieValue);
      eraseCookie(cookieName);
    }
  }


  export default migrateCookieToLocalStorage
  