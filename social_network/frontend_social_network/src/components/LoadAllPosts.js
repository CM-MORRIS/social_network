
// document.addEventListener('DOMContentLoaded', function() {


//     loadAllPosts();

// });

// function loadAllPosts() {

//     fetch('/all_posts')
//     .then(response => response.json())
//     .then(allPosts => {

//         // logs to console, for debugging purposes
//         console.log(allPosts);

//         for (post of allPosts) {

//             const post_id = post.post_id;
//             const username = post.username;
//             const text = post.text;
//             const date_time = post.date_time;
//             const number_of_likes = post.number_of_likes;
            
//             // creating a div (to hold each post)
//             let element = document.createElement('div');
//             element.id = `${post_id}.post`;

//             // date time posted
//             element.innerHTML += ` Posted: <p> ${date_time} </p> `;

//             // username
//             element.innerHTML += ` Username: <p> ${username} </p> `;

//             // post_text
//             let post_text = document.createElement('p');
//             post_text.id = `${post_id}.post_text`;
//             post_text.innerHTML = ` <p> ${text} </p> `;
//             element.appendChild(post_text);

//             // like_count
//             let like_count = document.createElement('p');
//             like_count.id = `${post_id}.like_count`;
//             like_count.innerHTML = ` ${number_of_likes} `;
//             element.appendChild(like_count);

//             // like button
//             let likeButton = document.createElement('button');
//             likeButton.className = "btn btn-sm btn-outline-primary";
//             likeButton.innerHTML = "Like";
//             likeButton.addEventListener('click', () => likePost(`${post_id}`));
//             element.appendChild(likeButton);

//             // add single post
//             document.querySelector('#display-all-posts').append(element);

//         }
//     });
// }

// function likePost(post_id) {

//     let csrftoken = Cookies.get('csrftoken');

//     fetch(`/like_post/${post_id}`, {
//         method: 'PUT',
//         headers: { "X-CSRFToken": csrftoken },
//     })
//     .then(response => response.json())
//     .then(response => {
//         console.log(response);
        
//         // update like count without reloading page
//         var post = document.getElementById(`${post_id}.like_count`);
//         post.innerHTML = response.like_count;

//     });
// }
