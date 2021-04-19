import React, { Component } from "react";
import axiosInstance from "../axiosApi";
import UserPost from "./UserPost";
import CreatePost from "./CreatePost";

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      allPosts: [],
    };
  }

  async getAllPosts() {
    try {
      let response = await axiosInstance.get("all_posts/");

      this.setState({
        allPosts: response.data.map((post) => ({
          postId: post.pk,
          userId: post.user_id,
          username: post.username,
          text: post.text,
          dateTime: post.date_time,
          likes: post.number_of_likes,
        })),
      });

      console.log(response.data);
    } catch (error) {
      console.log(error.stack);
    }
  }

  componentDidMount() {
    this.getAllPosts();
  }

  // every component needs a render to display whatever the component is
  render() {
    return (
      <div>
        {/* <div>{ <CreatePost/> }</div> */}
        {this.state.allPosts.map((post) => (
          <div key={post.pk}>
            <UserPost
              postId={post.postId}
              userId={post.userId}
              username={post.username}
              text={post.text}
              dateTime={post.dateTime}
              likes={post.likes}
            />
          </div>
        ))}
      </div>
    );
  }
}

// always have to export component from file
export default Home;
