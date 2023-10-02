from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


class EPortfolio(CanvasObject):
    def __str__(self):
        return "{}".format(self.name)

    def delete(self, **kwargs):
        """
        Delete an ePortfolio.

        :calls: `DELETE /api/v1/eportfolios/:id \
            <https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.delete>`_

        :returns: ePortfolio with deleted date set.
        :rtype: :class:`canvasapi.eportfolio.EPortfolio`
        """
        response = self._requester.request(
            "DELETE", "eportfolios/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )
        return EPortfolio(self._requester, response.json())

    def get_eportfolio_pages(self, **kwargs):
        """
        Return a list of pages for an ePortfolio.

        :calls: `GET /api/v1/eportfolios/:eportfolio_id/pages \
            <https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.pages>`_

        :returns: List of ePortfolio pages.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.eportfolio.EPortfolioPage`
        """

        return PaginatedList(
            EPortfolioPage,
            self._requester,
            "GET",
            "eportfolios/{}/pages".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def moderate_eportfolio(self, **kwargs):
        """
        Update the spam_status of an eportfolio.
        Only available to admins who can `moderate_user_content`.

        :calls: `PUT /api/v1/eportfolios/:eportfolio_id/moderate \
            <https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.moderate>`_

        :returns: Updated ePortfolio.
        :rtype: :class:`canvasapi.eportfolio.EPortfolio`
        """
        response = self._requester.request(
            "PUT",
            "eportfolios/{}/moderate".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return EPortfolio(self._requester, response.json())

    def restore(self, **kwargs):
        """
        Restore an ePortfolio back to active that was previously deleted.
        Only available to admins who can moderate_user_content.

        :calls: `PUT /api/v1/eportfolios/:eportfolio_id/restore \
            <https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.restore>`_

        :returns: Updated ePortfolio.
        :rtype: :class:`canvasapi.eportfolio.EPortfolio`
        """
        response = self._requester.request(
            "PUT",
            "eportfolios/{}/restore".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return EPortfolio(self._requester, response.json())


class EPortfolioPage(CanvasObject):
    def __str__(self):
        return "{}. {}".format(self.position, self.name)
