import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';

import axios from 'axios';
import UsersList from './components/UserList';
import About from './components/About';
import NavBar from './components/NavBar';
import Form from './components/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';

class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: '',
      title: 'awesomebane.io',
      isAuthenticated: false
    }
    this.logoutUser = this.logoutUser.bind(this);
    this.loginUser = this.loginUser.bind(this);
  };

  componentDidMount() {
    this.getUsers();
  };

  componentWillMount() {
    if (window.localStorage.getItem('authToken')) {
      this.setState({ isAuthenticated: true });
    }
  };

  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
    .then((res) => { this.setState({users: res.data.data.users})})
    .catch((err) => console.log(err))
  };

  loginUser(token) {
    window.localStorage.setItem('authToken', token);
    this.setState({ isAuthenticated: true });
    this.getUsers();
  }

  logoutUser() {
    window.localStorage.clear();
    this.setState({isAuthenticated: false});
  };

  render(){
    return (
      <div>
        <NavBar title={this.state.title} isAuthenticated={this.state.isAuthenticated}/>
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <br />
              <Switch>
                <Route exact path='/' render={() => (
                  <div>
                    <UsersList users={this.state.users}/>
                  </div>
                )} />
                <Route exact path='/about' component={About} />
                <Route exact path='/register' render={() => {
                    return (<Form
                      formType='Register'
                      formData={this.state.formData}
                      handleFormChange={this.handleFormChange}
                      handleUserFormSubmit={this.handleUserFormSubmit}
                      isAuthenticated={this.state.isAuthenticated}
                    />)
                }} />
                <Route exact path="/login" render={() => {
                  return (<Form
                    formType='Login'
                    formData={this.state.formData}
                    handleFormChange={this.handleFormChange}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    isAuthenticated={this.state.isAuthenticated}
                  />)
                }} />
              <Route exact path="/logout" render={() => {
                  return (
                    <Logout
                      logoutUser={this.logoutUser}
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )
              }} />
              <Route exact path="/status" render={() => {
                  return <UserStatus isAuthenticated={this.state.isAuthenticated}/>
              }} />
              </Switch>
            </div>
          </div>
        </div>
      </div>
    );

  }

}

export default App;
