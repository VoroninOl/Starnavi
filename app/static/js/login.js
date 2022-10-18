

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




$('#login-submit').on('click', () =>{
    const login = $('[name="login"]').val()
    const password = $('[name="password"]').val()
    $.ajax({
        type: "POST",
        url: 'login',
        data: JSON.stringify({'login': login, 'password': password}),
        dataType: 'json',
        success: (data) => {
            localStorage.setItem('Authorization', data.token)
            window.location = ('/')
        },
        error: (response) => {
            warnings.updateMessages([response.responseText])
        }
    })
})