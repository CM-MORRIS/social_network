import React, { Component } from "react";
import axiosInstance from "../axiosApi";
import SinglePost from "./SinglePost";

class Profile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      userId: "",
      username: this.props.match.params.username,
      followers: "",
      following: "",
      firstName: "",
      lastName: "",
      email: "",
      userPosts: [],

    };

    this.handleChange = this.handleChange.bind(this);

  }

  handleChange(event) {
    this.setState({ [event.target.name]: event.target.value });
  }

  componentDidMount() {
  
    this.getUserPosts();
    this.getUserDetails();
    this.getFollowers();
    this.getFollowing();
  }

  async getFollowers() {
    // check user exists otherwise go to home ? TODO
    const username = this.state.username;

    try {
      const response = await axiosInstance.get(`user_followers/${username}`);

      this.setState({
        followers: response.data["followersCount"],
      });
    } catch (error) {
      console.log(error.stack);
    }
  }

  async getFollowing() {
    // check user exists otherwise go to home ? TODO
    const username = this.state.username;

    try {
      const response = await axiosInstance.get(`user_following/${username}`);

      this.setState({
        following: response.data["followingCount"],
      });
    } catch (error) {
      console.log(error.stack);
    }
  }

  async getUserDetails() {
    // check user exists otherwise go to home ? TODO
    const username = this.state.username;

    try {
      const response = await axiosInstance.get(`user/${username}`);

      this.setState({
        userId: response.data["id"],
        firstName: response.data["first_name"],
        lastName: response.data["last_name"],
        email: response.data["email"],
      });

    } catch (error) {
      console.log(error.stack);
    }
  }

  async getUserPosts() {

    const username = this.state.username;

    console.log("username: " + username)
    try {
      let response = await axiosInstance.get(
        // `user_posts/${this.state.username}`
        `user_posts/${username}`

      );

      this.setState({
        userPosts: response.data.map((post) => ({
          postId: post.pk,
          userId: post.user_id,
          username: post.username,
          text: post.text,
          dateTime: post.date_time,
          likes: post.number_of_likes,
        }))
      });

    } catch (error) {
      console.log(error.stack);
    }
  }

  // every component needs a render to display whatever the component is
  render() {
    return (
      <div>
        <div>
          <li>
            {" "}
            User ID:
            {this.state.userId}
          </li>
          <li>
            {" "}
            Username:
            {this.state.username}
          </li>
          <li>
            First Name:
            {this.state.firstName}
          </li>
          <li>
            Last Name:
            {this.state.lastName}
          </li>
          <li>
            Email:
            {this.state.email}
          </li>
          <li>
            Following:
            {this.state.following}
          </li>
          <li>
            {" "}
            Followers:
            {this.state.followers}
          </li>
        </div>

        <div>Follow</div>

        {this.state.userPosts.map((post) => (
          <div key={post.pk}>
            <SinglePost
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
export default Profile;
