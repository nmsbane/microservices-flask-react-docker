import React from 'react';
import { shallow, mount } from 'enzyme';
import { MemoryRouter as Router } from 'react-router-dom';
import App from '../../App';

beforeAll(() => {
  global.localStorage = {
    getItem: () => {
      return 'sometoken'
    }
  }
});

test('App renders without crashing', () => {
  const wrapper = shallow(<App />, {disableLifecycleMethods:true});
});
