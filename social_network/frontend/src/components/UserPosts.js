import React, { Component } from "react";
import { Switch, Route, Link } from "react-router-dom";
import axiosInstance from "../axiosApi";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Profile from "./Profile";

class UserPosts extends Component {
  constructor(props) {
    super(props);
    this.state = {
      postId: "",
      userId: "",
      username: props.username,
      text: "",
      likes: "",
      dateTime: "",
      userPosts: [],
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ [event.target.name]: event.target.value });
  }

  async handleClick() {
    const postId = this.state.postId;

    try {
      let response = await axiosInstance.put(`like_post/${postId}`);

      this.setState({ likes: response.data.like_count });
    } catch (error) {
      console.log(error.stack);
    }
  }

  async getUserPosts() {
    // TODO causing an infinite loop
    try {
      let response = await axiosInstance.get(
        `user_posts/${this.state.username}`
      );

      this.setState({
        userPosts: response.data.map((post) => ({
          postId: post.pk,
          userId: post.user_id,
          username: post.username,
          text: post.text,
          dateTime: post.date_time,
          likes: post.number_of_likes,
        })),
      });
    } catch (error) {
      console.log(error.stack);
    }
  }

  render() {
    return (
      <div>
        {this.state.userPosts.map((post) => (
          <div key={post.pk}>
            <Card style={{ width: "18rem" }}>
              <Card.Body>
                <Card.Title>
                  <Link
                    className={"nav-link"}
                    to={`/profile/${this.props.username}`}
                  >
                    {this.props.username}
                  </Link>
                </Card.Title>
                <Card.Subtitle className="mb-2 text-muted">
                  {this.state.dateTime}
                </Card.Subtitle>
                <Card.Text>{this.state.text}</Card.Text>
                <Button onClick={this.handleClick} variant="dark">
                  Like
                </Button>
                <Card.Subtitle
                  className="mb-2 text-muted"
                  onChange={this.handleChange}
                >
                  {this.state.likes}
                </Card.Subtitle>
              </Card.Body>

              <Route path="/profile/:username" component={Profile} />
            </Card>
          </div>
        ))}
      </div>
    );
  }
}

export default UserPosts;
