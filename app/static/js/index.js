
const postBox = new Vue({
    el: '#div-posts-box',
    delimiters: ['[[',']]'],
    data: {
        posts: [],
    },
    methods: {
        // Updating info in chats
        updatePosts: (data) => {
            postBox.posts = data
        },
        likePost: (post) => {
            $.ajax({
                type: "POST",
                url: 'like_unlike_post',
                dataType: 'json',
                data: JSON.stringify({'token': localStorage.getItem('Authorization'), 'post_id': post.post_id}),
                success: (data) => {
                    if (post.liked){
                        post.likes = post.likes - 1
                        post.liked = false
                    }
                    else{
                        post.likes = post.likes + 1
                        post.liked = true
                    }
                },
                error: (response) => {
                    console.log(response)
                }
            })
        }
    }
})


function getPosts(){
    $.ajax({
        type: "GET",
        url: 'get_posts',
        data: {'token': localStorage.getItem('Authorization')},
        success: (data) => {
            postBox.updatePosts(data.posts)
        },
        error: (response) => {
            console.log(response)
            window.location = ('/login')
        }
    })
}


// Function just to test
function getAnalytics(){
    $.ajax({
        type: "GET",
        url: 'api/analytics',
        data: {'date_from': '2022-09-20', 'date_to': '2022-10-19'},
        success: (data) => {
            console.log(data)
        },
        error: (response) => {
            console.log(response)
        }
    })
}


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


getPosts()