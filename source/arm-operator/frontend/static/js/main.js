function addDeleteBtn(infoContainer, value, formToHide) {
    const deleteButton = document.createElement("button")

    deleteButton.className = 'new-obj'
    deleteButton.style.marginBottom = '10px'
    deleteButton.style.marginTop = '5px'
    deleteButton.innerHTML = "Удалить"
    deleteButton.addEventListener('click', deleteCarFromDiv)
    deleteButton.value = value
    deleteButton.formToHide = formToHide
    deleteButton.style.fontSize = '13px'

    infoContainer.appendChild(deleteButton)
}

function makeError(message, containerId) {
    const container = document.querySelector(containerId)
  
      const error = document.createElement("div")
      error.setAttribute('class', 'error-server')
      error.setAttribute('id', message)
  
      error.innerHTML = message
      const sameMessage = document.getElementById(message)
      if (!sameMessage) {
        container.appendChild(error)
      }
}

function addShowStreamBtn(infoContainer) {
    const deleteButton = document.createElement("button")

    deleteButton.className = 'new-obj'
    deleteButton.style.marginBottom = '10px'
    deleteButton.style.marginTop = '5px'
    deleteButton.innerHTML = "Отобразить поток"
    deleteButton.addEventListener('click', showStream)
    deleteButton.style.fontSize = '13px'

    infoContainer.appendChild(deleteButton)
}

function GetFaceInfo(value) {
    const infoContainer = document.querySelector("#info-face")
    
    infoContainer.style.display = 'inline-block'
    infoContainer.innerHTML = value

    addDeleteBtn(infoContainer, value, "#info-face")
}

function GetCarInfo(value) {
    const infoContainer = document.querySelector("#info-car")

    infoContainer.style.display = 'inline-block'
    infoContainer.innerHTML = value

    addDeleteBtn(infoContainer, value, "#info-car")
}

function GetStreamInfo(value) {
    const infoContainer = document.querySelector("#info-stream")
    infoContainer.style.display = 'inline-block'
    infoContainer.innerHTML = value

    const onAnalitics = document.createElement('input')
    const offAnalitics = document.createElement('input')

    const onAnaliticsLabel = document.createElement('label')
    const offAnaliticsLabel = document.createElement('label')

    const onAnaliticsP = document.createElement('p')
    const offAnaliticsP = document.createElement('p')

    offAnaliticsP.style.margin = '0'
    onAnaliticsP.style.margin = '0'

    onAnalitics.name = 'analitics'
    offAnalitics.name = 'analitics'

    onAnalitics.id = 'on-analitics'
    offAnalitics.id = 'off-analitics'

    onAnaliticsLabel.setAttribute('for', 'on-analitics')
    offAnaliticsLabel.setAttribute('for', 'off-analitics')

    offAnaliticsLabel.innerHTML = 'Включить аналитику'
    onAnaliticsLabel.innerHTML = 'Выключить аналитику'

    offAnaliticsLabel.style.paddingLeft = '5px'
    onAnaliticsLabel.style.paddingLeft = '5px'

    onAnalitics.type = 'radio'
    offAnalitics.type = 'radio'

    onAnalitics.addEventListener('change', setAnaliticsMode)
    offAnalitics.addEventListener('change', setAnaliticsMode)

    offAnaliticsP.appendChild(offAnalitics)
    offAnaliticsP.appendChild(offAnaliticsLabel)

    onAnaliticsP.appendChild(onAnalitics)
    onAnaliticsP.appendChild(onAnaliticsLabel)

    infoContainer.appendChild(onAnaliticsP)
    infoContainer.appendChild(offAnaliticsP)

    addShowStreamBtn(infoContainer)
    addDeleteBtn(infoContainer, value, "#info-stream")
}

function setAnaliticsMode(evt) {
    if (evt.target.id === 'on-analitics') {
        // onAnalitics()
    } else {
        // offAnalitics()
    }
}

function deleteCarFromDiv(evt) {
    const carToDelete = evt.currentTarget.value
    const formToHide = evt.currentTarget.formToHide

    const form = document.querySelector(formToHide)
    const optToDelete = document.querySelector('#'+carToDelete)

    optToDelete.remove()
    form.style.display = 'none'
}

function showStream() {
    const container = document.querySelector('.container-video')
    const streamVideo = document.createElement('video')

    container.appendChild(streamVideo)
}

async function AddPerson() {
    const newPersonInput = document.getElementById('new-person-name')
    const newPhotoInput = document.querySelector('#new-photo')
    const newPersonName = newPersonInput.value
    const newPhoto = newPhotoInput.files[0]

    let data = new FormData()
    data.append('person_data', JSON.stringify({name: newPersonName}))
    data.append('file', newPhoto)
    console.log(...data)

    if (newPersonName != '' && newPhoto != undefined) {
        await fetch("/add_person", {
            method: 'post',
            body: data
        }).then(function(response) {
            if (response.ok) {
                alert("Успешно добавлен человек")
            }
            else {
                alert(response.json())
            }
        })
        // addNewName(person)
    } else if (newPhoto == undefined) {
        makeError('Добавьте фото', '#new-person-container')
    } else if (newPersonName == '') {
        makeError('Введите имя', '#new-person-container')
    }
}

function AddCar() {
    const newCarInput = document.querySelector('#new-car')

    const newCar = newCarInput.value
    if (newCar != '') {
        // addNewName(newCar)
    } else {
        makeError('Введите машину', '#new-car-container')
    }
}

function AddStream() {
    const newStreamInput = document.querySelector('#new-stream-input')

    const newStream = newStreamInput.value
    if (newStream === '') {
        makeError('Введите ссылку для потока', '#new-stream-container')
    } else {
        // addNewStream(stream)
    }
}

// добавить новый видеопоток

// async function addNewStream(stream) {
//     const response = await fetch('/add_stream', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//         body: JSON.stringify(stream)
//       })
// }

// добавление нового человека 

// async function addNewName(name) {
//     const response = await fetch('/add_name', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//         body: JSON.stringify(name)
//       })
// }

// добавление новой машины

// async function addNewCar(car) {
//     const response = await fetch('/add_car', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//         body: JSON.stringify(car)
//       })
// }

// получать информацию о человеке по имени

// async function getInfoByName(name) {
//     const response = await fetch('/get_name', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//         body: JSON.stringify(name)
//       })
// }

// получать информацию о машине по номеру

// async function getInfoByCar(car) {
//     const response = await fetch('/get_car', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//         body: JSON.stringify(car)
//       })
// }

// удалить номер машины из бд

// async function deleteCar() {
//     const response = await fetch('/delete_car', {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//       })
// }

// удалить человека из бд

// async function deleteFace() {
//     const response = await fetch('/delete_face', {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//       })
// }

// включить режим аналитики

// async function onAnalitics() {
//     const response = await fetch('/delete_face', {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//       })
// }

// выключить режим аналитики

// async function offAnalitics() {
//     const response = await fetch('/delete_face', {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8'
//         },
//       })
// }
