let registrationFlag = false
let submitFlag = true
let error = 0

class Login {
  constructor(form, fields) {
    this.form = form;
    this.fields = fields;
    this.validateOnSubmit();
  }

  validateOnSubmit() {
    let self = this; // setup calls to the "this" values of the class described in the constructor

    this.form.addEventListener("submit", (e) => {
      e.preventDefault();
      let error = 0;
      self.fields.forEach((field) => {
        const input = document.querySelector(`#${field}`);
        if (self.validateFields(input) === false) {
          error++;
        }
      });
      if (error === 0) {
        const password = document.querySelector('#password')
        const login = document.querySelector('#login')

        let user = {
          password: password.value,
          login: login.value
        }
        if (registrationFlag) {
          signup(user)
        } else if (submitFlag) {
          registry(user)
        }
      }
    });
  }

  validateFields(field) {
    if (field.value.trim() === "") {
      setStatus(
        field,
        `${field.previousElementSibling.innerText} не может быть пустым`,
        "error"
      );
      return false;
    } else {
      if (field.type === "password") {
        if (field.value.length < 8) {
          setStatus(
            field,
            `${field.previousElementSibling.innerText} должен состоять минимум из 8 символов`,
            "error"
          );
          return false;
        } else {
          setStatus(field, null, "success");
          return true;
        }
      } else {
        setStatus(field, null, "success");
        return true;
      }
    }
  }
}

function checkAll() {
  clearServerErrors()
  const form = document.querySelector(".loginForm");
  if (form) {
    const fields = ["login", "password"];
    const validator = new Login(form, fields);

    if (registrationFlag) {
      const password = document.querySelector("#password")
      const repeatPassword = document.querySelector("#repeat-password-input")

      if (password.value !== repeatPassword.value) {
        setStatus(repeatPassword, "Пароли не совпадают", "error")
      }
    }
  }
}

function clearAll() {
  const password = document.querySelector("#password")
  const login = document.querySelector("#login")
  const errorMessagesForInput = document.querySelectorAll(".error-message")

  errorMessagesForInput.forEach(function(errorMessage) {
    errorMessage.innerHTML = ""
  })

  password.value = ""
  login.value = ""
}

function clearServerErrors() {
  const errorMessagesFromServers = document.querySelectorAll(".error-server")

  if (errorMessagesFromServers) {
    errorMessagesFromServers.forEach(error => {
      error.remove()
    })
  }
}

function setStatus(field, message, status) {
  const errorMessage = field.parentElement.querySelector(".error-message");

  error = 1;

  if (status === "success") {
    if (errorMessage) {
      errorMessage.innerText = "";
    }
    field.classList.remove("input-error");
  }
  if (status === "error") {
    errorMessage.innerText = message;
    field.classList.add("input-error");
  }
}

async function registry(user) {
  const response = await fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(user)
  })

  const text = await response.json();
  if (text.status == 'ok') {
    window.location.href = text.message
  } else {
    makeError(text.message)
  }
}

async function signup(user) {
  const response = await fetch('/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(user)
  })
  const text = await response.json();
  if (text.status == 'ok') {
    window.location.href = text.message
  } else {
    makeError(text.message)
  }
}

async function LogOut() {
   await fetch('/logout', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    }
  })
  .then(response => {
    if (response.redirected) {
      window.location.href = response.url
    }
  })
}

function makeError(message) {
  const container = document.querySelector('.input-data')

    const error = document.createElement("div")
    error.setAttribute('class', 'error-server')
    error.setAttribute('id', message)

    error.innerHTML = message
    const sameMessage = document.getElementById(message)
    if (!sameMessage) {
      container.appendChild(error)
    }
}

function Submit() {
  const authButton = document.querySelector("#submit")
  const loginButton = document.querySelector("#login-mode")

  const registryButton = document.querySelector("#registry-entry-btn")

  const repeatPassword = document.querySelector("#repeat-password")

  registrationFlag = false
  submitFlag = true

  clearAll()
  clearServerErrors()

  if (repeatPassword) {
    repeatPassword.remove()
  }
  authButton.style.color = "black"
  loginButton.style.color = "grey"

  registryButton.innerHTML = "Войти"
  registryButton.style.width = "25%"
}

function Enter() {
  registrationFlag = true
  submitFlag = false

  clearAll()
  clearServerErrors()

  if (! document.querySelector("#repeat-password")) {
    const authButton = document.querySelector("#submit")
    const loginButton = document.querySelector("#login-mode")

    const registryButton = document.querySelector("#registry-entry-btn")

    const container = document.querySelector(".input-data")

    const repeatPassword = document.createElement("div")
    const repeatPasswordInput = document.createElement("input")
    const repeatPasswordLabel = document.createElement("label")
    const repeatPasswordError = document.createElement("span")

    repeatPasswordInput.setAttribute("id", "repeat-password-input")
    repeatPasswordInput.setAttribute("type", "password")
    repeatPasswordInput.setAttribute("class", "input")

    repeatPassword.setAttribute("class", "input-group")
    repeatPassword.setAttribute("id", "repeat-password")

    repeatPasswordLabel.setAttribute("class", "label")
    repeatPasswordLabel.setAttribute("for", "repeat-password")
    repeatPasswordLabel.innerText = 'Повторите пароль'

    repeatPasswordError.setAttribute("class", "error-message")

    repeatPassword.appendChild(repeatPasswordLabel)
    repeatPassword.appendChild(repeatPasswordInput)
    repeatPassword.appendChild(repeatPasswordError)

    container.appendChild(repeatPassword)

    authButton.style.color = "grey"
    loginButton.style.color = "black"

    registryButton.innerHTML = "Зарегистрироваться"
    registryButton.style.width = "50%"
  }
}
