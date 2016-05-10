from canvas_object import CanvasObject


class Module(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s, description: %s" % (
            self.id,
            self.name,
            self.description
        )

    def edit(self, course_id, **kwargs):
        """
        Update and return an existing module

        :calls: `PUT /api/v1/courses/:course_id/modules/:id`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update>
        :rtype: :class:`Module`
        """
        from module import Module

        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s' % (course_id, self.id),
            **kwargs
        )
        return Module(self._requester, response.json())

    def delete(self, course_id):
        """
        Delete a module


        :calls: `DELETE /api/v1/courses/:course_id/modules/:id`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.destroy>
        :rtype: :class:`Module`
        """
        from module import Module

        response = self._requester.request(
            'DELETE',
            'courses/%s/modules/%s' % (course_id, self.id),
        )
        return Module(self._requester, response.json())

    def relock(self, course_id):
        """
        Resets module progressions to their default locked state and recalculates
        them based on the current requirements.

        Adding progression requirements to an active course will notlock students
        out of modules they have already unlocked unless this action is called.

        :calls: `PUT /api/v1/courses/:course_id/modules/:id/relock`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.relock>
        :rtype: :class:`Module`
        """
        from module import Module

        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s/relock' % (course_id, self.id),
        )
        return Module(self._requester, response.json())


class ModuleItem(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s, description: %s" % (
            self.id,
            self.name,
            self.description
        )

