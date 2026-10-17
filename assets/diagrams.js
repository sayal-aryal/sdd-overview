// The guide stays readable if the optional diagram renderer is unavailable.
const diagrams = [...document.querySelectorAll('.mermaid')];
const sources = diagrams.map(node => node.textContent);
try {
  const { default: mermaid } = await import('https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs');
  mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base',
    themeVariables: { primaryColor: '#eaf0e7', primaryTextColor: '#20342e',
      primaryBorderColor: '#9ab59f', lineColor: '#66776e', fontFamily: 'system-ui, sans-serif',
      fontSize: '14px', signalColor: '#31513e' },
    flowchart: { useMaxWidth: false }, sequence: { useMaxWidth: false } });
  await mermaid.run({ nodes: diagrams });
} catch (error) {
  diagrams.forEach((node, index) => {
    node.textContent = sources[index];
    node.removeAttribute('data-processed');
    node.closest('figure').querySelector('figcaption').textContent =
      'Diagram source · visual rendering is unavailable. Try again with an internet connection.';
  });
  console.warn('Mermaid diagrams could not be rendered.', error);
}

const links = [...document.querySelectorAll('nav a')];
const observer = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    links.forEach(link => {
      if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
}, { rootMargin: '-10% 0px -70% 0px' });
document.querySelectorAll('h2[id]').forEach(heading => observer.observe(heading));
