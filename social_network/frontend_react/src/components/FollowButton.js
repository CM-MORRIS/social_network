import React, { Component } from "react";
import { Switch, Route, Link } from "react-router-dom";
import axiosInstance from "../axiosApi";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Profile from "./Profile";


class FollowButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
        userProfile: props.userProfile, 
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);

  }

  handleChange(event) {
    this.setState({ [event.target.name]: event.target.value });
  }

  componentDidMount() {

    this.isFollowing();
  
    // follow
    // unfollow
    // no button
    // implemented the is_following to chek sttaus of button TODO
  }

  async handleClick() {

    const userProfile = this.state.userProfile;

    try {

      let response = await axiosInstance.put(`like_post/${postId}`);

      this.setState({ likes: response.data.like_count });

    } catch (error) {
      console.log(error.stack);
    }
  }

  async isFollowing() {

    const userProfile = this.state.userProfile;

    try {

        let response = await axiosInstance.get(`is_following/${userProfile}`)

        console.log("response.data['isFollowing']: " + response.data["isFollowing"]);
        console.log("response['isFollowing']: " + response["isFollowing"]);
        console.log("this.state.userProfile: " + this.state.userProfile);


        return response.data["isFollowing"];
        

    } catch (error) {
      console.log(error.stack);
    }
  }

  // check: logged in user vs user profile 
  // if following show 'unfollow'
  // if not following show 'follow'

  render() {
    return (

      <div>Follow</div>

    );
  }
}

export default FollowButton;
