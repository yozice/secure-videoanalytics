function addDeleteBtn(infoContainer, value, formToHide) {
    const deleteButton = document.createElement("button")

    deleteButton.className = 'new-obj'
    deleteButton.style.marginBottom = '10px'
    deleteButton.style.marginTop = '5px'
    deleteButton.innerHTML = "Удалить"
    if (formToHide === '#info-car') {
        deleteButton.addEventListener('click', deleteCar)
    } else if (formToHide === '#info-face') {
        deleteButton.addEventListener('click', deletePerson)
    } else if (formToHide === '#info-stream') {
        deleteButton.addEventListener('click', deleteStream)
    }
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

function addShowStreamBtn(infoContainer, value) {
    const showButton = document.createElement("button")

    showButton.className = 'new-obj'
    showButton.style.marginBottom = '10px'
    showButton.style.marginTop = '5px'
    showButton.innerHTML = "Отобразить поток"
    showButton.addEventListener('click', showStream)
    showButton.value = value
    showButton.style.fontSize = '13px'

    infoContainer.appendChild(showButton)
}

async function GetFaceInfo(value) {
    const infoContainer = document.querySelector("#info-face")
    
    infoContainer.style.display = 'inline-block'
    infoContainer.innerHTML = value
    let personId;
    let personName;
    await fetch(`/get_person_info/${value}`)
        .then((response) => response.json())
        .then((data) => {
        personId = data['id']
        personName = data['name']
        // personPhoto = data['photo']
    })
        
    infoContainer.innerHTML += personId 
    infoContainer.innerHTML += personName 
    // const img = document.createElement('img')
    // img.src = personPhoto
    // img.height = 'auto'
    // img.width = '100%'

    addDeleteBtn(infoContainer, value, "#info-face")
}

async function GetCarInfo(value) {
    const infoContainer = document.querySelector("#info-car")

    infoContainer.style.display = 'inline-block'
    infoContainer.innerHTML = value

    let autoId;
    let autoNumber;
    let autoModel;

    await fetch(`/get_auto_info/${value}`)
        .then((response) => response.json())
        .then((data) => {
            autoId = data['id']
            autoNumber = data['number']
            autoModel = data['model']
        })
    infoContainer.innerHTML += autoId 
    infoContainer.innerHTML += autoNumber 
    infoContainer.innerHTML += autoModel

    addDeleteBtn(infoContainer, value, "#info-car")
}

function GetStreamInfo(value) {
    const infoContainer = document.querySelector("#info-stream")
    infoContainer.style.display = 'inline-block'
    infoContainer.innerHTML = value

    // const onAnalitics = document.createElement('input')
    // const offAnalitics = document.createElement('input')

    // const onAnaliticsLabel = document.createElement('label')
    // const offAnaliticsLabel = document.createElement('label')

    // const onAnaliticsP = document.createElement('p')
    // const offAnaliticsP = document.createElement('p')

    // offAnaliticsP.style.margin = '0'
    // onAnaliticsP.style.margin = '0'

    // onAnalitics.name = 'analitics'
    // offAnalitics.name = 'analitics'

    // onAnalitics.id = 'on-analitics'
    // offAnalitics.id = 'off-analitics'

    // onAnaliticsLabel.setAttribute('for', 'on-analitics')
    // offAnaliticsLabel.setAttribute('for', 'off-analitics')

    // offAnaliticsLabel.innerHTML = 'Включить аналитику'
    // onAnaliticsLabel.innerHTML = 'Выключить аналитику'

    // offAnaliticsLabel.style.paddingLeft = '5px'
    // onAnaliticsLabel.style.paddingLeft = '5px'

    // onAnalitics.type = 'radio'
    // offAnalitics.type = 'radio'

    // onAnalitics.addEventListener('change', setAnaliticsMode)
    // offAnalitics.addEventListener('change', setAnaliticsMode)

    // offAnaliticsP.appendChild(offAnalitics)
    // offAnaliticsP.appendChild(offAnaliticsLabel)

    // onAnaliticsP.appendChild(onAnalitics)
    // onAnaliticsP.appendChild(onAnaliticsLabel)

    // infoContainer.appendChild(onAnaliticsP)
    // infoContainer.appendChild(offAnaliticsP)

    addShowStreamBtn(infoContainer, value)
    addDeleteBtn(infoContainer, value, "#info-stream")
}

function setAnaliticsMode(evt) {
    if (evt.target.id === 'on-analitics') {
        // onAnalitics()
    } else {
        // offAnalitics()
    }
}

async function deletePerson(evt) {
    const personToDelete = evt.currentTarget.value
    const formToHide = evt.currentTarget.formToHide
    
    let personId;

    const response = await fetch('/get_person_info/' + personToDelete, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
      })
    const text = await response.json();
    personId = text.id

    if (personId != undefined) {
        await fetch('/rm_person/' + personId, {
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json;charset=utf-8'
            },
        }).then(function(response) {
        console.log(response)
        if(response.ok) {
            const form = document.querySelector(formToHide)
            const optToDelete = document.querySelector('#'+personToDelete)

            optToDelete.remove()
            form.style.display = 'none'
        } else {
            alert(response.json().message)
        }
        })
    }
}

async function deleteCar(evt) {
    const carToDelete = evt.currentTarget.value
    const formToHide = evt.currentTarget.formToHide
    
    let carId;

    const response = await fetch('/get_auto_info/' + carToDelete, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
      })
    const text = await response.json();
    carId = text.id
    
    if (carId != undefined) {
        await fetch('/rm_auto/' + carId, {
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json;charset=utf-8'
            },
        }).then(function(response) {
        console.log(response)
        if(response.ok) {
            const form = document.querySelector(formToHide)
            const optToDelete = document.querySelector('#'+carToDelete)

            optToDelete.remove()
            form.style.display = 'none'
        } else {
            alert(response.json().message)
        }
        })
    }
}

async function deleteStream(evt) {
    const streamToDelete = evt.currentTarget.value
    const formToHide = evt.currentTarget.formToHide
    
    // console.log(streamToDelete)
    let streamId;

    const response = await fetch('/get_video_stream_info/' + streamToDelete, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
      })
    const text = await response.json();
    streamId = text.id
    
    if (streamId != undefined) {
        await fetch('/rm_video_stream/' + streamId, {
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json;charset=utf-8'
            },
        }).then(function(response) {
        console.log(response)
        if(response.ok) {
            const form = document.querySelector(formToHide)
            const optToDelete = document.querySelector('#'+streamToDelete)

            optToDelete.remove()
            form.style.display = 'none'
        } else {
            alert(response.json().message)
        }
        })
    }
}

async function showStream(evt) {
    const stream = evt.currentTarget.value
    const container = document.querySelector('.container-video')

    let streamVideo

    const response = await fetch('/get_video_stream_info/' + stream, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
      })
    const streamInfo = await response.json();
    streamVideo = streamInfo.video   

    const streamVideoElement = document.createElement('video')

    streamVideoElement.src = streamVideo
    streamVideo.autoplay = false
    streamVideo.controls = true
    streamVideo.height = 240
    streamVideo.width = 320
    container.appendChild(streamVideoElement)
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
                alert(response.json().message)
            }
        })
        // addNewName(person)
    } else if (newPhoto == undefined) {
        makeError('Добавьте фото', '#new-person-container')
    } else if (newPersonName == '') {
        makeError('Введите имя', '#new-person-container')
    }
}

async function AddCar() {
    const newCarNumber = document.getElementById('new-car-number').value
    const newCarModel = document.getElementById('new-car-model').value

    if (newCarNumber != '' && newCarModel != '') {
        await fetch("/add_auto", {
            method: "post",
            headers: {"content-type": 'application/json'},
            body: JSON.stringify({number: newCarNumber, model: newCarModel})
        }).then(function(response) {
            if (response.ok) {
                alert("Успешно добавлено авто")
            }
            else {
                alert(response.json().message)
            }
        })       
    } else {
        makeError('Введите данные автомобиля', '#new-car-container')
    }
}

async function AddStream() {
    const newStreamName = document.getElementById('new-stream-name').value
    const newStreamUrl = document.getElementById('new-stream-url').value

    if (newStreamName === '' && newStreamUrl === '') {
        makeError('Введите данные о потоке для потока', '#new-stream-container')
    } else {
        // addNewStream(stream)
        await fetch("/add_video_stream", {
            method: "post",
            headers: {"content-type": 'application/json'},
            body: JSON.stringify({name: newStreamName, url: newStreamUrl})
        }).then((response) => {
            if (response.ok) {
                alert("Успешно добавлен поток")
            }
            else {
                alert("Не удалось добавить поток")
            }
        })
    }
}
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
