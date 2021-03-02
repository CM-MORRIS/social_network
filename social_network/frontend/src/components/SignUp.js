import React, { Component } from "react";
import axiosInstance from "../axiosApi";

class Signup extends Component {
    constructor(props){
        super(props);

        this.state = {

            firstName: "",
            lastName: "",
            username: "",
            email:"",
            password: "",
            confirmPassword: ""
            
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    async handleSubmit(event) {
        event.preventDefault();

        try {
            const response = await axiosInstance.post('/register_user/', {
                first_name: this.state.firstName,
                last_name: this.state.lastName,
                username: this.state.username,
                email: this.state.email,
                password: this.state.password,
                confirm_password: this.state.confirmPassword
            });
            return response;

        } catch (error) {
            console.log(error.stack);
            this.setState({
                errors:error.response.data
            });
        }
    }

    render() {
        return (
            <div>
                Signup
                <form onSubmit={this.handleSubmit}>
                    <label>
                        First name:
                        <input name="firstName" type="text" value={this.state.firstName} onChange={this.handleChange}/>
                        {/* { this.state.errors.firstName ? this.state.errors.firstName : null} */}
                    </label>
                    <label>
                        Last name:
                        <input name="lastName" type="text" value={this.state.lastName} onChange={this.handleChange}/>
                        {/* { this.state.errors.lastName ? this.state.errors.lastName : null} */}
                    </label>
                    <label>
                        Username:
                        <input name="username" type="text" value={this.state.username} onChange={this.handleChange}/>
                        {/* { this.state.errors.username ? this.state.errors.username : null} */}
                    </label>
                    <label>
                        Email:
                        <input name="email" type="email" value={this.state.email} onChange={this.handleChange}/>
                        {/* { this.state.errors.email ? this.state.errors.email : null} */}
                    </label>
                    <label>
                        Password:
                        <input name="password" type="password" value={this.state.password} onChange={this.handleChange}/>
                        {/* { this.state.errors.password ? this.state.errors.password : null} */}
                    </label>
                    <label>
                        Confirm Password:
                        <input name="confirmPassword" type="password" value={this.state.confirmPassword} onChange={this.handleChange}/>
                    </label>

                    <input type="submit" value="Submit"/>
                </form>
            </div>
        )
    }
}
export default Signup;