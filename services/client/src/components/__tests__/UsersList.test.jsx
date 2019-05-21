import React from 'react';
import { shallow } from 'enzyme';

import UsersList from '../UsersList';
import renderer from 'react-test-renderer';

const users = [
  {
    'active': true,
    'email': 'josvillegas@upeu.edu.pe',
    'id': 1,
    'username': 'jos'
  },
  {
    'active': true,
    'email': 'tofoshi@gmail.com',
    'id': 2,
    'username': 'toshi'
  }
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('jos');
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});