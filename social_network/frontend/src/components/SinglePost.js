import React, { Component } from "react";
import axiosInstance from "../axiosApi";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

class SinglePost extends Component {
  constructor(props) {
    super(props);
    this.state = {
      postId: props.postId,
      username: props.username,
      text: props.text,
      likes: props.likes,
      dateTime: props.dateTime,
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

  render() {
    return (
      <Card style={{ width: "18rem" }}>
        <Card.Body>
          <Card.Title>{this.state.username}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted">
            {this.state.dateTime}
          </Card.Subtitle>
          <Card.Text>{this.state.text}</Card.Text>
          <Button onClick={this.handleClick} variant="dark">
            Like
          </Button>
          <Card.Subtitle className="mb-2 text-muted" onChange={this.handleChange}>
            {this.state.likes}
          </Card.Subtitle>
        </Card.Body>
      </Card>
    );
  }
}

export default SinglePost;
