
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


$('#register-submit').on('click', () =>{
    const login = $('[name="login"]').val()
    const password = $('[name="password"]').val()
    const password2 = $('[name="password"]').val()
    if (password != password2){
        warnings.updateMessages(['Passwords do not matches!'])
        return null
    }
    $.ajax({
        type: "POST",
        url: 'register',
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