import React, { useState, useEffect } from "react";
import Button from "@material-ui/core/Button";
import Menu from "@material-ui/core/Menu";
import { Switch, Route, Link } from "react-router-dom";
import axiosInstance from "../axiosApi";


import MenuItem from "@material-ui/core/MenuItem";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import { makeStyles } from "@material-ui/core/styles";
import Profile from "./Profile";

export default function SimpleMenu() {

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

const [anchorEl, setAnchorEl] = useState(null);
const [loggedInUser, setLoggedInUser] = useState(null);


const handleClick = (event) => {
  setAnchorEl(event.currentTarget);
};

const handleClose = () => {
  setAnchorEl(null);
};

const getLoggedInUser = async () => {
  const response = await axiosInstance.get("/get_logged_in_user/");

  // const data = await response.json();
  setLoggedInUser(response.data["user_logged_in"]);

};

useEffect(() => {
  getLoggedInUser();
});

const classes = useStyles();

  return (
    <div>
      <IconButton
        edge="start"
        onClick={handleClick}
        className={classes.menuButton}
        color="inherit"
        aria-label="menu"
      >
        <MenuIcon />
      </IconButton>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem onClick={handleClose}>
          <Link className={"nav-link"} to={"/home"}>
            Home
          </Link>
        </MenuItem>

        <MenuItem onClick={handleClose}>
          <Link className={"nav-link"} to={"/signup/"}>
            Signup
          </Link>
        </MenuItem>

        <MenuItem onClick={handleClose}>
          <Link className={"nav-link"} to={"/login/"}>
            Login
          </Link>
        </MenuItem>

        <MenuItem onClick={handleClose}>
          <Link className={"nav-link"} to={"/new-post/"}>
            Post
          </Link>
        </MenuItem>

        <MenuItem onClick={handleClose}>
            <Link className={"nav-link"} to={`/profile/${loggedInUser}`}>
              {loggedInUser}
            </Link>
        </MenuItem>

      </Menu>
    </div>
  );
}
