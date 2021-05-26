import React, { Component } from "react";
import ReactDom from 'react-dom';
import axiosInstance from "../axiosApi";

const constants = {
    MIN_CHARACTERS: 1,
    MAX_CHARACTERS: 280
  };

class CreatePost extends Component {

    constructor(props) {
        super(props);
        this.state = 
        {   
            postText: "" 
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }


    handleChange(event) {
        this.setState({ postText: event.target.value });
    }


    async handleSubmit(event) {

        event.preventDefault();

        if (this.state.postText.length >= constants.MIN_CHARACTERS && 
            this.state.postText.length <= constants.MAX_CHARACTERS) {

            alert("Valid submission");

            try {
            
                const response = await axiosInstance.post('create_post/', {
                    text: this.state.postText
                });

                // empty text input after submit
                this.setState({ postText: ''});

                return response;

            } catch (error) {
                console.log(error.stack);
                
            }

        }
        else {
            alert("invalid submission");
        }
    }

    render() {
        return (

            <div>Create Post
                <form onSubmit={this.handleSubmit}>
                    <textarea name="post" type="text" value={this.state.postText} onChange={this.handleChange} />
                    <input type="submit" value="Post"/>
                </form>
            </div>
        );
    }

}

export default CreatePost;