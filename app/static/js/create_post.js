
const warnings = new Vue({
    el: '#div-warnings',
    delimiters: ['[[',']]'],
    data: {
        warningMessages: [],
    },
    methods: {
        updateMessages: (data) => {
            warnings.warningMessages = data
        },
    }
})

$('#create-post-submit').on('click', () =>{
    const header = $('[name="header"]').val()
    const content = $('[name="content"]').val()
    $.ajax({
        type: "POST",
        url: 'create_post',
        data: JSON.stringify({'token': localStorage.getItem('Authorization'), 'header': header, 'content': content}),
        dataType: 'json',
        success: (data) => {
            // localStorage.setItem('Authorization', data.token)
            window.location = ('/')
        },
        error: (response) => {
            warnings.updateMessages([response.responseText])
        }
    })
})


$('#logout').on('click', () =>{
    $.ajax({
        type: "POST",
        url: 'logout',
        data: JSON.stringify({'token': localStorage.getItem('Authorization')}),
        success: (data) => {
            localStorage.removeItem('Authorization')
            window.location = ('/')
        },
        error: (response) => {
            window.location = ('/')
            console.log(response)
        }
    })
})
