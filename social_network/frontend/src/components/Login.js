import React, { Component } from "react";
import axiosInstance from "../axiosApi";

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = 
        {   username: "", 
            password: ""
        };

        /*
            onChange property to a method called handleChange.
            Whenever content of input changes, when a keystroke occurs,
            it triggers the handleChange method to do what we want it to do, which is to update the local 
            component state to match the entered text value for each input field using setState
         */
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    // handleSubmit(event) {
    //     event.preventDefault();
    //     try {
    //         const response = axiosInstance.post('/token/obtain/', {
    //             username: this.state.username,
    //             password: this.state.password
    //         });
    //         axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
    //         localStorage.setItem('access_token', response.data.access);
    //         localStorage.setItem('refresh_token', response.data.refresh);

    //         console.log("login_refresh_token:" + data.refresh);
    //         console.log("login_acess_token:" + data.access);

    //         return data;
    //     } catch (error) {
    //         throw error;
    //     }
    // }

    // Just need to add async at the beginning when declaring the method, 
    // and at the part you want the code to wait, add an await. 
    // It’s that easy. The rest of the code can be written like it’s synchronous, 
    // and that includes errors. Very clean.


    // use this new version over commented out one below '.then'

    async handleSubmit(event) {

        event.preventDefault();
        const response = await axiosInstance.post('/token/obtain/', {
            username: this.state.username,
            password: this.state.password
        });
        
        axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);

        window.location.reload();


        console.log("login_refresh_token handle submit:" + response.data.refresh);
        console.log("login_acess_token handle submit:" + response.data.access);

    
    } catch (error) {
        throw error;
    }

    render() {
        return (
            <div>Login
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Username:
                        <input name="username" type="text" value={this.state.username} onChange={this.handleChange}/>
                    </label>
                    <label>
                        Password:
                        <input name="password" type="password" value={this.state.password} onChange={this.handleChange}/>
                    </label>
                    <input type="submit" value="Submit"/>
                </form>
            </div>
        );
    }
}

export default Login;