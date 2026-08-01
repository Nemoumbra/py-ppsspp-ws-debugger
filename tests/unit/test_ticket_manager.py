
import pytest

from ppsspp.ticket_manager import TicketManager


# TODO: maybe parametrize the ticket length

def test_default_tickets():
    kTicketLength = 8
    ticket_man = TicketManager(ticket_length=kTicketLength)
    tickets = [ticket_man.get_ticket() for _ in range(10)]
    # Correct length
    for ticket in tickets:
        assert len(ticket) == kTicketLength

    for ticket in tickets:
        ticket_man.finalize_ticket(ticket)
        with pytest.raises(ValueError):
            # Can't finalize twice!
            ticket_man.finalize_ticket(ticket)


def test_custom_tickets():
    kTicketLength = 8
    ticket_man = TicketManager(ticket_length=kTicketLength)
    custom_tickets = [
        "", "123", "abc", "xyz0", "0" * 100
    ]
    for ticket in custom_tickets:
        with pytest.raises(ValueError):
            # No ticket yet
            ticket_man.finalize_ticket(ticket)
        ticket_man.add_custom_ticket(ticket)

        # Can't add it again!
        with pytest.raises(ValueError):
            ticket_man.add_custom_ticket(ticket)

    for ticket in reversed(custom_tickets):
        ticket_man.finalize_ticket(ticket)
        with pytest.raises(ValueError):
            # Can't finalize twice!
            ticket_man.finalize_ticket(ticket)


def test_any_tickets():
    kTicketLength = 8
    ticket_man = TicketManager(ticket_length=kTicketLength)
    custom_tickets = [
        "", "123", "abc", "xyz0", "0" * 100
    ]
    assert all(len(ticket) != kTicketLength for ticket in custom_tickets), "Your tests suck"

    custom_ticket_idx = 0
    tickets = []
    for i in range(2 * len(custom_tickets)):
        if i % 2 == 0:
            ticket = ticket_man.get_ticket()
        else:
            ticket = custom_tickets[custom_ticket_idx]
            custom_ticket_idx += 1

            with pytest.raises(ValueError):
                # No such ticket yet
                ticket_man.finalize_ticket(ticket)
            ticket_man.add_custom_ticket(ticket)

            # Can't add it again!
            with pytest.raises(ValueError):
                ticket_man.add_custom_ticket(ticket)

        tickets.append(ticket)

    for ticket in tickets:
        ticket_man.finalize_ticket(ticket)
        with pytest.raises(ValueError):
            # Can't finalize twice!
            ticket_man.finalize_ticket(ticket)

    pass


def test_repeated_tickets():
    kTicketLength = 8
    ticket_man = TicketManager(ticket_length=kTicketLength)

    custom_ticket = "abcd"
    ticket_man.add_custom_ticket(custom_ticket)
    ticket_man.finalize_ticket(custom_ticket)
    # Must work fine after being finalized
    ticket_man.add_custom_ticket(custom_ticket)
    ticket_man.finalize_ticket(custom_ticket)

    ticket = ticket_man.get_ticket()
    with pytest.raises(ValueError):
        ticket_man.add_custom_ticket(ticket)

    ticket_man.finalize_ticket(ticket)
    # Now it should succeed
    ticket_man.add_custom_ticket(ticket)
    ticket_man.finalize_ticket(ticket)


# This one shouldn't be parametrized
def test_low_keyspace():
    kTicketLength = 1
    ticket_man = TicketManager(ticket_length=kTicketLength)

    # Letters
    kIterations = 26 * 2

    tickets = [ticket_man.get_ticket() for _ in range(kIterations)]
    for ticket in tickets:
        ticket_man.finalize_ticket(ticket)
