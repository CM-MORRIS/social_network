import React, { Component} from "react";
import { Switch, Route, Link } from "react-router-dom";
import Login from "./Login";
import SignUp from "./Signup";
import Hello from "./Hello";
import CreatePost from "./CreatePost";
import Home from "./Home";
import axiosInstance from "../axiosApi";


class App extends Component {

    constructor() {
        super();
        this.handleLogout = this.handleLogout.bind(this);
    }

    async handleLogout() {
        try {
            const response = await axiosInstance.post('/blacklist/', {
                "refresh_token": localStorage.getItem("refresh_token")
            });
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            axiosInstance.defaults.headers['Authorization'] = null;
            return response;
        }
        catch (e) {
            console.log(e);
        }
    };

    render() {
        return (
            <div className="site">
                <nav>
                    <Link className={"nav-link"} to={"/home"}>Home</Link>
                    <Link className={"nav-link"} to={"/login/"}>Login</Link>
                    <Link className={"nav-link"} to={"/signup/"}>Signup</Link>
                    <Link className={"nav-link"} to={"/hello/"}>Hello</Link>
                    <Link className={"nav-link"} to={"/new-post/"}>Post</Link>

                    <button onClick={ this.handleLogout }>Logout</button>
                </nav>

                <main>
                    
                    {
                        /* <Switch> block which lets React know that in that 
                        space we will switch rendered components depending on 
                        the defined routes.  */
                    }

                    {
                        /* 'exact' property, when the URL path is matched exactly, 
                        the relevant component is rendered. All other paths go to home 
                        (or better yet, a future 404 page).  */
                    }

                    <Switch>
                        <Route exact path={ "/login/" } component={ Login }/>
                        <Route exact path={ "/signup/" } component={ SignUp }/>
                        <Route exact path={"/hello/"} component={ Hello }/>
                        <Route path={"/new-post"} component={ CreatePost }/>
                        <Route path={"/home"} component={ Home }/>

                   </Switch>
               </main>
            </div>
        );
    }
}

export default App;