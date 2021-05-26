import React, { useState, useEffect } from "react";
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Menu from './Menu';
import { Switch, Route, Link } from "react-router-dom";
import axiosInstance from "../axiosApi";


export default function ButtonAppBar() {

    const useStyles = makeStyles((theme) => ({
        root: {
          flexGrow: 1,
        },
        menuButton: {
          marginRight: theme.spacing(2),
        },
        title: {
          flexGrow: 1,
        },
    }));

    const classes = useStyles();


    const [isUserLoggedIn, setIsUserLoggedIn] = useState(null);

    
    const getIsUserLoggedIn = async () => {
      const response = await axiosInstance.get("/is_user_logged_in/");

      setIsUserLoggedIn(response.data["is_user_logged_in"]);
    };

    useEffect(() => {
        getIsUserLoggedIn();
    });

    const handleLogout = async () => {
        try {
            const response = await axiosInstance.post('/blacklist/', {
                "refresh_token": localStorage.getItem("refresh_token")
            });
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            axiosInstance.defaults.headers['Authorization'] = null;
            window.location.reload();
            return response;
        }
        catch (e) {
            console.log(e);
        }
    };


    function LogInButton(props) {

      const isLoggedIn = props.isLoggedIn

      if (isLoggedIn) {
        return (
            <Link to={"/login/"}>
              <Button onClick={handleLogout} variant="contained" color="secondary" disableElevation>
                Logout
              </Button>
            </Link>
          );
      }
      return (
        <Link to={"/login/"}>
          <Button variant="contained" color="secondary" disableElevation>
            Login
          </Button>
        </Link>
      );
    }

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>

                    <Menu/>

                    <Typography variant="h6" className={classes.title}>
                        Social Network
                    </Typography>
              
                    <LogInButton isLoggedIn={isUserLoggedIn}/>
                    
                </Toolbar>
            </AppBar>
        </div>
    );
}