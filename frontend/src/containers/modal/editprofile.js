import React, { Component } from 'react';
import { connect } from 'react-redux';
import EditProfile from '../../components/editprofile';
import Modal from '../../components/modal';
import {
  hideModal,
  showModal,
  editProfileReset
} from '../../actions';
import {
  editProfile
} from '../../api';

class EditProfileModal extends Component {
  componentWillMount() {
    if (!this.props.isAuthenticated) {
      this.props.handleClose();
    }
  }

  render() {
    const {
      isAuthenticated,
      isEditing,
      error,
      avatar,
      name,
      editProfile,
      handleClose,
      success
    } = this.props;

    return !isAuthenticated ? null : (
      <Modal
        onClose={handleClose}
        dialogStyle={{ width: '40%'}}
      >
        <EditProfile
          avatar={avatar}
          name={name}
          handleEdit={editProfile}
          isLoading={isEditing}
          error={error}
          success={success}
        />
      </Modal>
    );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated,
  isEditing: state.auth.isEditing,
  error: state.auth.editError,
  avatar: state.auth.avatar,
  name: state.auth.name,
  success: state.auth.editSuccess
});

const mapDispatchToProps = (dispatch) => ({
  editProfile: (newProfile) => {
    dispatch(editProfile(newProfile));
  },
  handleClose: () => {
    dispatch(hideModal());
    dispatch(editProfileReset());
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(EditProfileModal);
