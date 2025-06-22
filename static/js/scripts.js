$(document).ready(function() {
    $('a[href="/logout"]').click(function(e) {
        if (!confirm('Вы уверены, что хотите выйти из системы?')) {
            e.preventDefault();
        }
    });

    $('.edit-user-btn').click(function(){
        $('#editUserId').val($(this).data('userid'));
        $('#editUserName').val($(this).data('username'));
        $('#editUserEmail').val($(this).data('email'));
        $('#editUserRole').val($(this).data('role'));
        $('#editUserModal').modal('show');
    });

    $('.edit-subject-btn').click(function(){
        $('#editSubjectId').val($(this).data('subjectid'));
        $('#editSubjectTitle').val($(this).data('title'));
        $('#editSubjectDescription').val($(this).data('description'));
        $('#editSubjectModal').modal('show');
    });

    $('.edit-exercise-btn').click(function(){
        $('#editExerciseId').val($(this).data('exerciseid'));
        $('#editExerciseTitle').val($(this).data('title'));
        $('#editExerciseDescription').val($(this).data('description'));
        $('#editExerciseModal').modal('show');
    });

    $('.edit-submission-btn').click(function(){
        $('#editSubmissionId').val($(this).data('submissionid'));
        $('#editSubmissionModal').modal('show');
    });
});
