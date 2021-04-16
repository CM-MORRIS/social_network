import React, { Component} from "react";
import { Switch, Route, Link } from "react-router-dom";
import LoginForm from "./LoginForm";
import SignUp from "./Signup";
import Hello from "./Hello";
import CreatePost from "./CreatePost";
import Home from "./Home";
import Profile from "./Profile";
import NavBar from './NavBar';
import axiosInstance from "../axiosApi";


class App extends Component {

    constructor() {
        super();
        this.state =
        {   
            username: "",
        };

        this.handleChange = this.handleChange.bind(this);

    }

    handleChange(event) {
        this.setState({ username: event.target.value });
    }

    componentDidMount() {
  
        this.getLoggedInUser();
      }

    async getLoggedInUser() {

        try {
        
            const response = await axiosInstance.get('/get_logged_in_user/');

            if (response.status != 401) {
                this.setState({
                    username: response.data["user_logged_in"],
                });
            }

        }
        catch (e) {
            console.log(e);
        }

    }

    render() {
        return (
          <div className="site">

              <NavBar/>

           
            <main>
              {/* <Switch> block which lets React know that in that 
                        space we will switch rendered components depending on 
                        the defined routes.  */}

              {/* 'exact' property, when the URL path is matched exactly, 
                        the relevant component is rendered. All other paths go to home 
                        (or better yet, a future 404 page).  */}

              <Switch>

                <Route exact path={"/login/"} component={LoginForm} />
                <Route exact path={"/signup/"} component={SignUp} />
                <Route exact path={"/hello/"} component={Hello} />
                <Route path={"/new-post"} component={CreatePost} />
                <Route path={"/home"} component={Home} />
                <Route path={"/profile/:username"} component={Profile} />

              </Switch>
            </main>
          </div>
        );
    }
}

export default App;