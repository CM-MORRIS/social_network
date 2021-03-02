import React, { Component } from "react";
import { Switch, Route, Link } from "react-router-dom";
import axiosInstance from "../axiosApi";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Profile from "./Profile";


class SinglePost extends Component {
  constructor(props) {
    super(props);
    this.state = {
      postId: props.postId,
      userId: props.userId,
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
          <Card.Title>

          <Link className={"nav-link"} to={`/profile/${this.props.username}`}>{this.props.username}</Link>
                    
          </Card.Title>
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

            
            {/* <Route  path={`/profile/${this.state.username}`} 
                    render={
                        (props) => <Profile {...props} userId={this.state.userId} />
            } /> */}

            {/* <Route path="/profile/:username" component={Profile}/> */}

      </Card>

    );
  }
}

export default SinglePost;
