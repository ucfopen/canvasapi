from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs, obj_or_str


class Feature(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.display_name, self.applies_to)

    @property
    def _parent_id(self):
        """
        Return the id of the account, course or user that spawned this feature

        :rtype: int
        """
        if hasattr(self, "account_id"):
            return self.account_id
        elif hasattr(self, "course_id"):
            return self.course_id
        elif hasattr(self, "user_id"):
            return self.user_id
        else:
            raise ValueError(
                "Feature Flag does not have account_id, course_id or user_id"
            )

    @property
    def _parent_type(self):
        """
        Return whether the feature with the feature was spawned from an account,
        a course or a user.

        :rtype: str
        """
        if hasattr(self, "account_id"):
            return "account"
        elif hasattr(self, "course_id"):
            return "course"
        elif hasattr(self, "user_id"):
            return "user"
        else:
            raise ValueError(
                "Feature Flag does not have account_id, course_id or user_id"
            )


class FeatureFlag(CanvasObject):
    def __str__(self):
        return "{} {} {} {}".format(
            self.context_type, self.context_id, self.feature, self.state
        )

    def delete(self, feature, **kwargs):
        """
        Remove a feature flag for a given account, course or user.

        :calls: `DELETE /api/v1/courses/:course_id/features/flags/:feature \
            <https://canvas.instructure.com/doc/api/
            feature_flags.html#method.feature_flags.delete>`_

            or `DELETE /api/v1/accounts/:account_id/features/flags/:feature \
            <https://canvas.instructure.com/doc/api/
            feature_flags.html#method.feature_flags.delete>`_

            or `DELETE /api/v1/users/:user_id/features/flags/:feature \
            <https://canvas.instructure.com/doc/api/
            feature_flags.html#method.feature_flags.delete>`_

        :rtype: :class:`canvasapi.feature.FeatureFlag`
        """
        feature_name = obj_or_str(feature, "name", (Feature,))

        response = self._requester.request(
            "DELETE",
            "{}s/{}/features/flags/{}".format(
                feature._parent_type, feature._parent_id, feature_name
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return FeatureFlag(self._requester, response.json())

    def set_feature_flag(self, feature, **kwargs):
        """
        Set a feature flag for a given account, course or user.

        :calls: `PUT /api/v1/courses/:course_id/features/flags/:feature \
            <https://canvas.instructure.com/doc/api/
            feature_flags.html#method.feature_flags.update>`_

            or `PUT /api/v1/accounts/:account_id/features/flags/:feature \
            <https://canvas.instructure.com/doc/api/
            feature_flags.html#method.feature_flags.update>`_

            or `PUT /api/v1/users/:user_id/features/flags/:feature \
            <https://canvas.instructure.com/doc/api/
            feature_flags.html#method.feature_flags.update>`_

        :param feature: The feature object to set
        :type feature: :class:`canvasapi.feature.Feature`

        :rtype: :class:`canvasapi.feature.FeatureFlag`
        """
        feature_name = obj_or_str(feature, "name", (Feature,))

        response = self._requester.request(
            "PUT",
            "{}s/{}/features/flags/{}".format(
                feature._parent_type, feature._parent_id, feature_name
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return FeatureFlag(self._requester, response.json())
