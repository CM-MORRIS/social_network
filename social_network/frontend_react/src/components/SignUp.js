import React, { Component } from "react";
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

    firstName: yup
        .string('Enter your first name')
        .max(15, "Must be 15 characters or less")
        .required('Required'),
    lastName: yup
        .string('Enter your last name')
        .max(30, "Must be 15 characters or less")
        .required('Required'),
    username: yup
        .string('Enter your username')
        .min(5, "Must be minimum 5 characters")
        .max(20, "Must be 20 characters or less")
        .matches(
            /^(?=[a-zA-Z0-9._]{5,20}$)(?!.*[_.]{2})[^_.].*[^.]$/,
            "Invalid username"
        )
        .test(
            "userNameExists",
            "User already exists",

            async function (value) {
                const response = await axiosInstance.get(
                    `/user_exists/${value}`
                );
                return !response.data.exists;
            }
        )
        .required('Required'),
    email: yup
        .string('Enter your email')
        .email('Enter a valid email')
        .test(
            "emailExists",
            "Account with that email already exists",
            async function (value) {
                const response = await axiosInstance.get(
                    `/email_exists/${value}`
                );
                return !response.data.exists;
            }
        )
        .required('Required'),
    password: yup
        .string('Enter your password')
        .min(5, "Must be minimum 5 characters")
        .matches(
            /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{5,}$/,
            "Must be a mix of uppercase, lowercase, numbers, and special characters"
        )
        .required('Required'),
    passwordConfirmation: yup
        .string("Please confirm password")
        .oneOf([yup.ref("password"), null], "Passwords must match")
        .required('Required'),
  });
  
  const WithMaterialUI = () => {
    const formik = useFormik({
      initialValues: {
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        password: '',
        passwordConfirmation: '',

      },
      validationSchema: validationSchema,
      onSubmit: async (values) => {

        try {
            const response = await axiosInstance.post('/register_user/', {
                first_name: values.firstName,
                last_name: values.lastName,
                username: values.username,
                email: values.email,
                password: values.password,
                confirm_password: values.passwordConfirmation
            });

        } catch (error) {
            console.log(error.stack);
        }
        alert(JSON.stringify(values, null, 2));
      },
    });
  
    const classes = useStyles();

    return (

        <form onSubmit={formik.handleSubmit}>

        <Box className={classes.root}>
        
            <TextField
                size="medium"
                id="outlined-error-helper-text"
                name="firstName"
                label="First name"
                value={formik.values.firstName}
                onChange={formik.handleChange}
                error={formik.touched.firstName && Boolean(formik.errors.firstName)}
                helperText={formik.touched.firstName && formik.errors.firstName}
                variant="outlined"
                className={clsx(classes.margin, classes.textField)}
            />
                    
            <TextField
                size="medium"
                id="outlined-error-helper-text"
                name="lastName"
                label="Last Name"
                value={formik.values.lastName}
                onChange={formik.handleChange}
                error={formik.touched.lastName && Boolean(formik.errors.lastName)}
                helperText={formik.touched.lastName && formik.errors.lastName}
                variant="outlined"
                className={clsx(classes.margin, classes.textField)}
            />
            
            <TextField
                id="outlined-error-helper-text"
                name="email"
                label="Email"
                value={formik.values.email}
                onChange={formik.handleChange}
                error={formik.touched.email && Boolean(formik.errors.email)}
                helperText={formik.touched.email && formik.errors.email}
                variant="outlined"
                className={clsx(classes.margin, classes.textField)}
            />
            
            <TextField
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

            <TextField
                id="outlined-error-helper-text"
                name="passwordConfirmation"
                label="Confirm Password"
                type="password"
                value={formik.values.passwordConfirmation}
                onChange={formik.handleChange}
                error={formik.touched.passwordConfirmation && Boolean(formik.errors.passwordConfirmation)}
                helperText={formik.touched.passwordConfirmation && formik.errors.passwordConfirmation}
                variant="outlined"
                className={clsx(classes.margin, classes.textField)}
            />
         
            <MyButton type="submit">
                Create Account
            </MyButton>

        </Box>

          <Divider className={classes.divider} />

        </form>

        
    );
  };

export default WithMaterialUI;
