import React from 'react';

const AddUser = (props) => {
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
            />
        </div>
        <input
            type="submit"
            className="btn btn-primary btn-lg btn-block"
            type="submit"
          />
      </form>
  )

};

export default AddUser;
