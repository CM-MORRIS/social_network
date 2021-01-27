
// document.addEventListener('DOMContentLoaded', function() {
    
//     // Select the submit button and text input to be used
//     const submit_post = document.querySelector('#submit-post');
//     const post_text = document.querySelector('#new-post-body');

//     // Disable submit post button by default:
//     submit_post.disabled = true;

//     // Listen for input to be typed into the post text field
//     post_text.onkeyup = () => {
        
//         if (post_text.value.trim().length > 0) {
//             submit_post.disabled = false;
//         } else {
//             submit_post.disabled = true;
//         }
//     }

//     submit_post.addEventListener('click', () => {

//         /*
//         Fetch is a Javascript function that accepts two arguments.
//         1:  URL as String,
//         2:  Optional argument that contains info about the request.
//         If you are only looking to retrieve data from an API,
//         you do not need to use the second argument, as Javascript will automatically
//         expect a “GET” request.
//         */

//         let post_data = {
//             text: post_text.value
//         };
        
//         // need to parse csrf token in header when POST forms for secutiy reasons
//         let csrftoken = Cookies.get('csrftoken');

//         fetch('/create_post', {
//             method: 'POST',
//             body: JSON.stringify(post_data),
//             headers: { "X-CSRFToken": csrftoken },
//         })
//         .then(response => response.json())
//         .then(result => {
//             console.log(result);
//         });
//     });

// });
