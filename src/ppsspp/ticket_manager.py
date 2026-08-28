
from random import choices
from string import ascii_letters, digits


class TicketManager:
    def __init__(self, ticket_length: int):
        self._char_pool = ascii_letters + digits
        self._unresolved_tickets: set[str] = set()
        self.ticket_length: int = ticket_length

    def _make_ticket(self):
        ticket = "".join(choices(self._char_pool, k=self.ticket_length))
        while ticket in self._unresolved_tickets:
            ticket = "".join(choices(self._char_pool, k=self.ticket_length))

        return ticket

    def get_ticket(self):
        ticket = self._make_ticket()
        # We know 'ticket' is not there.
        self._unresolved_tickets.add(ticket)
        return ticket

    def add_custom_ticket(self, ticket: str):
        if ticket in self._unresolved_tickets:
            raise ValueError(f"Ticket '{ticket}' already known!")
        self._unresolved_tickets.add(ticket)

    def finalize_ticket(self, ticket: str):
        if ticket not in self._unresolved_tickets:
            raise ValueError(f"Ticket '{ticket}' was not expected!")
        self._unresolved_tickets.remove(ticket)
