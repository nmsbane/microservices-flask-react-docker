import React from 'react';

const AddUser = (props) => {
  console.log(props);
  // eslint-disable-next-line
      return (
        <form onSubmit={(event) => props.addUser(event)}>
        <div className="form-group">
          <input
            name="username"
            className="form-control input-lg"
            type="text"
            placeholder="Enter a username"
            required
            onChange={props.handleChange}
            value={props.username}
            key="0"
            />
        </div>
        <div className="form-group">
          <input
            name="email"
            className="form-control input-lg"
            type="email"
            placeholder="Enter an email address"
            required
            onChange={props.handleChange}
            value={props.email}
            key="1"
            />
        </div>
          <input
            key="2"
            type="submit"
            className="btn btn-primary btn-lg btn-block"
            type="submit" />
      </form>
    );

};

export default AddUser;
