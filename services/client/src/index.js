import React, { Component } from 'react';
import ReactDom from 'react-dom';
import axios from 'axios';

import UserList from './components/UserList';
import AddUser from './components/AddUser';

class App extends Component {
    constructor(){
      super();
      this.state = {
        users: [],
        username: '',
        email: ''
      };
      this.addUser = this.addUser.bind(this);
      this.handleChange = this.handleChange.bind(this);
    }

    render() {
      return (
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <br />
              <h1>All Users</h1>
              <hr /><br />
              <AddUser
                addUser={this.addUser}
                username={this.state.username}
                email={this.state.email}
                handleChange={this.handleChange}
              />
              <br />
              <UserList users={this.state.users} />
            </div>
          </div>
        </div>
      )
    }

    componentDidMount() {
        this.getUsers();
    }

    addUser(event) {
      event.preventDefault();
      const data = {
        username: this.state.username,
        email: this.state.email
      }
      axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then((res) => {
        this.getUsers();
        this.setState({ username: '', email: '' });
      })
      .catch((err) => { console.log(err); });
    };

    getUsers() {
      console.log(process.env);
      axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
        .then((res) => { this.setState({ users: res.data.data.users} )})
        .catch((err) => { console.log(err);})
    }

    handleChange(event) {
      const obj = {};
      obj[event.target.name] = event.target.value;
      this.setState(obj);
    }
}

ReactDom.render(
  <App />,
  document.getElementById('root')
);
