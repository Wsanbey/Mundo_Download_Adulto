$(document).ready(function() {
    var carousel = new bootstrap.Carousel(document.querySelector('#partnerSites'), {
        interval: 3000,
        wrap: true
    });

    $('#downloadBtn').click(function() {
        const url = $('#url').val();

        if (!url) {
            alert('Please enter a URL.');
            return;
        }

        $('#downloadBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...');


        $.ajax({
            url: '/baixar_video',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ url: url }),
            success: function(response) {
                const linksList = $('#linksList');
                linksList.empty(); // Limpa a lista de links

                if (response.links && response.links.length > 0) {
                    response.links.forEach(function(link) {
                        // Adiciona um item de lista que redireciona para a página de downloads
                        linksList.append('<li class="list-group-item"><a href="/downloads?link=' + encodeURIComponent(link) + '" target="_blank"><i class="fas fa-download me-2"></i>Download</a></li>');
                    });
                } else {
                    linksList.append('<li class="list-group-item">No links found.</li>');
                }

                $('#downloadLinks').slideDown(); // Exibe a seção de links
                $('#downloadBtn').prop('disabled', false).text('Get Download Links');
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + xhr.responseJSON.error);
                $('#downloadBtn').prop('disabled', false).text('Get Download Links');
            }
        });
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});