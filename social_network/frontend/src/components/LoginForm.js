import React, { Component } from "react";
import { useHistory } from "react-router-dom";

import { Redirect } from "react-router-dom"
import clsx from 'clsx';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axiosInstance from "../axiosApi";
import {Form as BootstrapForm} from 'react-bootstrap'; // used alias as conflicts with formik 'Form'
import { useFormik } from 'formik';
import * as yup from 'yup';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { styled } from '@material-ui/core/styles';
import { makeStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import { spacing } from '@material-ui/system';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';


const MyButton = styled(Button) ({
    background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
    border: 0,
    borderRadius: 3,
    boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
    color: 'white',
    height: 48,
    padding: '0 30px',
    margin: 8
});

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        flexWrap: 'nowrap',
        paddingTop: 50,
        paddingBottom: 50,

    },
    textField: {
        width: '30ch',
    },
    margin: {
        margin: theme.spacing(1),
      },
    divider: {
        margin: theme.spacing(10, 0),
      },
}));


const validationSchema = yup.object({

    username: yup
        .string('Enter your username')
        .min(5, "Must be minimum 5 characters")
        .max(20, "Must be 20 characters or less")
        .matches(
            /^(?=[a-zA-Z0-9._]{5,20}$)(?!.*[_.]{2})[^_.].*[^.]$/,
            "Invalid username"
        )
        .required('Required'),
    password: yup
        .string('Enter your password')
        .min(5, "Must be minimum 5 characters")
        .required('Required'),
  });

  
  const WithMaterialUI = () => {
    let history = useHistory();

    const formik = useFormik({
      initialValues: {
        username: '',
        password: '',
      },
      validationSchema: validationSchema,

      onSubmit: async (values, { setErrors, resetForm }) => {

        try {

            const response = await axiosInstance.post('/token/obtain/', {
                username: values.username,
                password: values.password
            });

            console.log(">>>>>>>>")
            console.log(response.data)
            console.log(response.status)
            console.log(response)
            console.log(">>>>>>>>")

            axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
                
            // console.log("login_refresh_token handle submit:" + response.data.refresh);
            // console.log("login_access_token handle submit:" + response.data.access);

        } catch (error) {

            console.log("error.response.status: " + error.response.status);

            console.log(error.stack);

            setErrors({ username: 'Username or password incorrect' });

            return false;

            // set error message 
        }

        // refreshes and loads home page on successful login
        history.push(`/profile/${values.username}`);
        window.location.reload();
        return true;

      },
      
    });
  
    const classes = useStyles();

    return (

        <form onSubmit={formik.handleSubmit}>

        <Box className={classes.root}>
        
            <TextField
                size="medium"
                id="outlined-error-helper-text"
                name="username"
                label="Username"
                value={formik.values.username}
                onChange={formik.handleChange}
                error={formik.touched.username && Boolean(formik.errors.username)}
                helperText={formik.touched.username && formik.errors.username}
                variant="outlined"
                className={clsx(classes.margin, classes.textField)}
            />
                    
            <TextField
                size="medium"
                id="outlined-error-helper-text"
                name="password"
                label="Password"
                type="password"
                value={formik.values.password}
                onChange={formik.handleChange}
                error={formik.touched.password && Boolean(formik.errors.password)}
                helperText={formik.touched.password && formik.errors.password}
                variant="outlined"
                className={clsx(classes.margin, classes.textField)}
            />
         
            <MyButton type="submit">
                Login
            </MyButton>

        </Box>

          <Divider className={classes.divider} />

        </form>

        
    );
  };

export default WithMaterialUI;
